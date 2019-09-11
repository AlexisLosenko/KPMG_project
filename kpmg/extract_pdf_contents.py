import os
import spacy
from pymongo.errors import DuplicateKeyError
from spacy_langdetect import LanguageDetector
from pymongo import MongoClient
from wand.image import Image as WandImg
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe(LanguageDetector(), name="language_detector", last=True)

def pdfsToTxt(folderPath):
    files = []

    for r, d, f in os.walk(folderPath):
        for file in f:
            if ".pdf" in file:
                files.append(os.path.join(r, file))
    for f in files:
        pdf_img = Image.open(convert_to_img(f, 300))
        pdf_string = pytesseract.image_to_string(pdf_img)
        doc = nlp(pdf_string)

        pdf_text = encode_newlines(pdf_string)

        language = doc._.language["language"]
        txt_filename = format_txt_filename(f, language)
        txt_file = open(txt_filename, "w+")
        txt_file.write(pdf_text)
        print("Txt created: " + txt_filename)
        txt_file.close()

        statute_dict = {"_id" : os.path.basename(f).replace(".pdf", ""),
                        "pdf_txt_content" : pdf_text,
                        "language" : language}
        client = MongoClient()
        db = client.kpmg
        stat_coll = db.statutes
        try:
            insert_result = stat_coll.insert_one(statute_dict)
            if insert_result.acknowledged:
                print("Document inserted into db kmpg, collection statutes, with _id " + str(insert_result.inserted_id))
        except DuplicateKeyError as e :
            print("Id already in database: " + str(e))


def encode_newlines(text) :
    return text.replace("\\r\\n", "\r\n").replace("\\n", "\n").replace("\\r", "\r")

def remove_newlines(text) :
    return text.replace("\\r\\n", " ").replace("\\n", " ").replace("\\r", " ")

def format_txt_filename(original_pdf, language) :
    return os.path.abspath(original_pdf).replace(".pdf", "_").replace("\\pdf", "\\txt") + \
    language + \
    ".txt"

def convert_to_img(file, resolution) :
    file_path = os.path.abspath(file)
    img_path = file_path.replace("pdf", "png")

    if os.path.isfile(img_path):
        print("Image already exists: " + img_path)
    else :
        with WandImg(filename=file_path, resolution=resolution) as img:
            img.compression_quality = 99
            img.save(filename=img_path)
            print("Image created: " + img_path)

    return img_path


pdfsToTxt(".\\pdf")
