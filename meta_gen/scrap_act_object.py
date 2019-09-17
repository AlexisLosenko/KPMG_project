from lxml import etree
import requests
import json
import pandas as pd
from time import sleep

def act_obj(uid):
    sleep(0.5)
    url = f"https://www.ejustice.just.fgov.be/cgi_tsv/tsv_l_1.pl?lang=fr&sql=btw+contains+%27{uid}%27&fromtab=TSV&rech=1&pdda=&pddm=&pddj=&pdfa=&pdfm=&pdfj=&naam=&postkode=&localite=&numpu=&hrc=&akte=&btw={uid}&jvorm=&land=&set2=&set3="

    response = requests.get(url)
    dom = etree.HTML(response.text)

    try:
        value = dom.xpath('//tr[1]/td[2]/br[3]/following-sibling::text()[1]')[0]
    except IndexError:
        value = 'N/A'

    return value





