# KPMG Project

Project Team with Pierro Simon, Niels Steven, Sebastien Pardon, Kristof Nachtergaele, Marco Tampieri and Alexis Losenko

The goal of this project is to successfully gather files such as pdfs on Internet sites, convert them as a text file, and to be able to retrieve any desired or important information.


Database used: Mongodb on default port and localhost


#1 scraping_final folder. Run py files: 01, 02, 03                                            |      SCRAPING

#2 KPMG/kpmg folder. Scraped pdfs into pdf folder. Run extract_pdf_contents.py                |      OCR -> DATABASE INSERT

#3 meta_gen folder . Run update_db_with_meta.py                                               |      DATABASE UPDATE

#4 Article extraction folder. Run articles_extraction_1.0b.py                                 |      DIVIDE ARTICLES + TRANSLATE

Frontend is in front. Run with flask after database exists
    
## Front-end

 **Dependencies**
 
 In order for the front to work, make sure you have the following packages installed in the 'pymongoexample' dir:  
   `pipenv install flask flask-pymongo python-dotenv`  
 or  
 `pip install flask flask-pymongo python-dotenv`    
 Also make sure you have **mongoDb** installed on your machine  
   
 
 **Launching**   
   
 Depending on your mongodb settings or your OS, run the following line to start your mongodb:  
   `sudo service mongod start` (ubuntu)  
   
 To start the flask application, if everything went smoothly, run   
   `flask run` from your '*/front*' directory.    
