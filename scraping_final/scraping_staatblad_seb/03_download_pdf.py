#import wget
#import pandas as pd
import os.path
import time
import requests
from fake_useragent import UserAgent
#import random
import sys
import json



print('Beginning file download with wget module')

#urlstest = "http://www.ejustice.just.fgov.be/tsv_pdf/2019/01/03/19300336.pdf"

with open('link_pdf_2018.json', 'r') as f:
        urls = json.load(f)

#urls = pd.read_json('link_pdf_2018.json')
#urls.drop_duplicates(subset=None, keep='first', inplace=True)

#urls = urls[0].tolist()
ua = UserAgent()

for key in urls :
    try:
        time.sleep(0.1)
        print(f'trying: {urls[key]}')
        pdfname = str(urls[key]['source_date'])+'_'+str(urls[key]['VAT'])
        #print(pdfname)
        if os.path.exists('./pdf/'+str(pdfname)+'.pdf') is False:
            #wget.download(key, './pdf')
            #wget -O ./pdfname key

            myfile = requests.get(key, headers={'User-Agent': ua.random})
            print(f'yo : {key}')
            with open(f'pdf/{pdfname}.pdf', 'wb') as file:
                file.write(myfile.content)
        else:
            pass

    except:
        print(f'ERROR url: {key}')
        print(sys.exc_info())



