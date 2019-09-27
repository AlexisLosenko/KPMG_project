# KPMG Project

Project Team with Pierro Simon, Niels Steven, Sebastien Pardon, Kristof Nachtergaele, Marco Tampieri and Alexis Losenko

The goal of this project is to successfully gather files such as pdfs on Internet sites, convert them as a text file, and to be able to retrieve any desired or important information.


Database used: Mongodb on default port and localhost


#1 scraping_final folder. Run py files: 01, 02, 03                                            |      SCRAPING

#2 KPMG/kpmg folder. Scraped pdfs into pdf folder. Run extract_pdf_contents.py                |      OCR -> DATABASE INSERT

#3 meta_gen folder . Run update_db_with_meta.py                                               |      DATABASE UPDATE

#4 Article extraction folder. Run articles_extraction_1.0b.py                                 |      DIVIDE ARTICLES + TRANSLATE

Frontend is in front. Run with flask after database exists
