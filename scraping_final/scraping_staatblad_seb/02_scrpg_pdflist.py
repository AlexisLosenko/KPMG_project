import pandas as pd
import json
#import random
from fake_useragent import UserAgent 
import requests
#import urllib.request
#import time
from bs4 import BeautifulSoup
import re
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.exceptions import SSLError
from OpenSSL.SSL import SysCallError
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


urls = pd.read_json('link_01_2018.json')
urls = urls[0][:1000].tolist()

def link_pdf():
    ua = UserAgent()
    urls_pdf = {}
    for i in urls:
        try:
            response = requests.get(i,  headers={'User-Agent': ua.random}, verify=False)
            print(response)
            soup = BeautifulSoup(response.text, 'html.parser')

            for link in soup.findAll('a', attrs={'href': re.compile("pdf$")}):
                links = link.get('href')
                #urls_pdf.append([link.get('href'), i[-10:]])
                urls_pdf[link.get('href')] = {'VAT': i[-10:],
                                              'source_ref': links[-12:-4],
                                              'source_date': str(links[-23:-19])+str(links[-18:-16])+str(links[-15:-13])
                                              }

        except SysCallError :
            print(f"SysCallError for {i[-10]}")


    return urls_pdf

result = link_pdf()

with open('link_pdf_2018.json', 'w') as outfile:
    json.dump(result, outfile)  


