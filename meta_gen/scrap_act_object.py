from lxml import etree
import requests
import json
import pandas as pd
from time import sleep


##change path##
token = pd.read_json("C:/Users/sebch/Desktop/kpmg/Local Folder/sources/token.json")
### head() for testing to remove
token = token[0].head().to_list()

for i in token:
    sleep(1)
    url = f"https://www.ejustice.just.fgov.be/cgi_tsv/tsv_l_1.pl?lang=fr&sql=btw+contains+%27{i}%27&fromtab=TSV&rech=1&pdda=&pddm=&pddj=&pdfa=&pdfm=&pdfj=&naam=&postkode=&localite=&numpu=&hrc=&akte=&btw={i}&jvorm=&land=&set2=&set3="

    response = requests.get(url)
    dom = etree.HTML(response.text)

    dic_object = dict()
    dic_object['id'] = i
    dic_object['object'] = dom.xpath('//tr/td[2]/br[3]/following-sibling::text()[1]')[0]

    with open(f'object_json/{''0'+str(i)}.json', 'w') as fp:
        json.dump(dic_object, fp)

