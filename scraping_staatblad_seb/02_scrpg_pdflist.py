import pandas as pd
import json
import random
from fake_useragent import UserAgent 
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re


urls = pd.read_json('link_01.json')
urls = urls[0].tolist()

def link_pdf():
    ua = UserAgent()
    urls_pdf = []
    for i in urls:
        response = requests.get(i,  headers={'User-Agent': ua.random})
        print(response)
        soup = BeautifulSoup(response.text, 'html.parser')
        soup.findAll('a')

        for link in soup.find_all(href=re.compile("[0-9]+.pdf")):
            print(link.get('href'))
            urls_pdf.append(link.get('href'))

    return urls_pdf
  


result = link_pdf()

with open('link_pdf.json', 'w') as outfile:
    json.dump(result, outfile)  


