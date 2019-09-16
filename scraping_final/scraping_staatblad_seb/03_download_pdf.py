import wget
import pandas as pd
import os.path
import time
import requests
from fake_useragent import UserAgent
import random
import sys



print('Beginning file download with get module')

urlstest = "http://www.ejustice.just.fgov.be/tsv_pdf/2019/01/03/19300336.pdf"

urls = pd.read_json('link_pdf.json')
urls.drop_duplicates(subset=None, keep='first', inplace=True)

urls = urls[0].tolist()
ua = UserAgent()

for i in urls :
    try:
        time.sleep(0.1)
        print(f'trying: {i}')
        pdfname = i[-12:]
        if os.path.exists('./pdf/'+ str(pdfname)) is False:
            wget.download(i, '/home/sebchko/Desktop/KPMG/pdf/')
#            myfile = requests.get(i, headers={'User-Agent': ua.random})
            print(f'yo : {i}')
#            with open(f'pdf/{pdfname}', 'wb') as file:
#                file.write(myfile.content) 
        else:
            pass

    except:
        print(f'ERROR url: {i}')
        print(sys.exc_info())  

