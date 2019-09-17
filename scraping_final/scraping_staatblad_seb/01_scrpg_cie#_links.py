import scrapy
import json
import re
from utils.date import dategenerator
from bs4 import BeautifulSoup
import pandas as pd
# launch script : scrapy runspider THISFILE.py 
class BlogSpider(scrapy.Spider):
    name = 'DE STAATSBLADMONITOR 2018 '

    start_urls = []

    daterange = dategenerator()
    for date in daterange:
        start_urls.append('https://www.staatsbladmonitor.be/oprichtingen-bedrijven.html?datum='+date)


    data_final = []
    token = []

    def parse(self, response):
        for data in response.css('.data::text'):
            if re.match('^[0-9]+$', data.get()):
                self.data_final.append('https://www.staatsbladmonitor.be/bedrijfsfiche.html?ondernemingsnummer='+data.get())
                self.token.append(data.get())

        with open('link_01.json', 'w', encoding='utf-8') as f:
            json.dump(self.data_final, f, ensure_ascii=False, indent=4)

        with open('token.json', 'w', encoding='utf-8') as g:
            json.dump(self.token, g, ensure_ascii=False, indent=4)  
