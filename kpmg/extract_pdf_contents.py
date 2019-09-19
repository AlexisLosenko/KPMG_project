import os
import glob
import spacy
from pymongo.errors import DuplicateKeyError
from spacy_langdetect import LanguageDetector
from pymongo import MongoClient
from wand.image import Image as WandImg
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#SEB path  r'C:\Users\sebch\AppData\Local\Tesseract-OCR\tesseract.exe'
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe(LanguageDetector(), name="language_detector", last=True)

def pdfsToTxt(folderPath):
    files = []

    for r, d, f in os.walk(folderPath):
        for file in f:
            if ".pdf" in file:
                files.append(os.path.join(r, file))

    for f in files:
        existing_txts = glob.glob(format_txt_filename(f, "dummy").replace("dummy", "*"))
        if existing_txts :
            print("TXT file already exists, skipping text detection and db insertion")
        else:
            #extract text from images
            image_path_list = convert_to_images(f, 300)
            total_page_count = str(len(image_path_list))
            page_count = 0
            pdf_string = ""
            for image_path in image_path_list :
                page_count += 1
                pdf_img = Image.open(image_path)
                pdf_string += pytesseract.image_to_string(pdf_img)
                print("Processed page " + str(page_count) + "/" + total_page_count
                      + " (" + image_path + ")")

            #detect language
            doc = nlp(pdf_string)
            language = doc._.language["language"]

            #write txt
            txt_file_path = format_txt_filename(f, language)
            txt_file = open(txt_file_path, "w+", encoding='utf-8')
            txt_file.write(pdf_string)
            print("Txt created: " + txt_file_path)
            txt_file.close()

            #write to db
            vat_nr = os.path.basename(f).replace(".pdf", "")
            statute_dict = {"_id" : vat_nr,
                            "pdf_txt_content" : pdf_string,
                            "language" : language}
            client = MongoClient()
            db = client.kpmg
            stat_coll = db.statutes
            stat_doc = stat_coll.find_one({"_id": uid})
            if stat_doc:
                stat_coll.update_one({'_id': uid},
                                     {'$set': {
                                         f"documents.{date}": {'text': pdf_string, 'object': act_obj(uid[1:], date)}}},
                                     upsert=True
                                     )
            else:
                insert_result = stat_coll.insert_one(statute_dict)
                if insert_result.acknowledged:
                    print("Document inserted into db kmpg, collection statutes, with _id " + str(
                        insert_result.inserted_id))
            

def encode_newlines(text) :
    return text.replace("\\r\\n", "\r\n").replace("\\n", "\n").replace("\\r", "\r")

def remove_newlines(text) :
    return text.replace("\\r\\n", " ").replace("\\n", " ").replace("\\r", " ")

def format_txt_filename(original_pdf, language) :
    return os.path.abspath(original_pdf).replace(".pdf", "_").replace("\\pdf", "\\txt") + \
    language + \
    ".txt"

def convert_to_images(file, resolution) :
    file_path = os.path.abspath(file)
    img_path_template = file_path.replace("\\pdf", "\\png").replace(".pdf", "")

    image_paths = glob.glob(img_path_template + "*")
    if image_paths :
        print("Images for " + file_path + " already exist, skipping image conversion")
    else :
        with WandImg(filename=file_path, resolution=resolution) as source:
            source.compression_quality = 99
            images = source.sequence
            nr_of_pages = len(images)
            image_paths = []
            for i in range(nr_of_pages):
                img_path = img_path_template + "_" + str(i) + ".png"
                #croping pages (if first pages else the others)
                if i == 0:
                    images[i].crop(int(images[i].size[0] * 0.16), int(images[i].size[1] * 0.20), int(images[i].size[0] * 0.95),
                                int(images[i].size[1] * 0.92))
                else:
                    images[i].crop(int(images[i].size[0] * 0.16), int(images[i].size[1] * 0.052), int(images[i].size[0] * 0.95),
                                int(images[i].size[1] * 0.92))
                WandImg(images[i]).save(filename=img_path)
                image_paths.append(img_path)
            print("Image(s) created: " + str(image_paths))

    return image_paths


pdfsToTxt(".\\pdf")
