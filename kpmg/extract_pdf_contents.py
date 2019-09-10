import os
import textract
import spacy
from pymongo.errors import DuplicateKeyError
from spacy_langdetect import LanguageDetector
from pymongo import MongoClient

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe(LanguageDetector(), name="language_detector", last=True)

def pdfsToTxt(folderPath):
    files = []

    for r, d, f in os.walk(folderPath):
        for file in f:
            if ".pdf" in file:
                files.append(os.path.join(r, file))
    for f in files:
        pdf_extract = textract.process(f)
        doc = nlp(pdf_extract.decode("utf8"))
        pdf_text = encode_newlines(str(pdf_extract))

        language = doc._.language["language"]
        txt_file = open(format_txt_filename(f, language), "w+")
        txt_file.write(pdf_text)
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
                print("Document inserted into statute_txts with _id " + str(insert_result.inserted_id))
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


pdfsToTxt("C:\\KPMG\\kpmg\\pdf")
