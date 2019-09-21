from bs4 import BeautifulSoup as bs
import requests


def act_obj(uid, date):
    date = str(date)
    date_f = str(date)[:4]+'-'+str(date)[4:6]+'-'+str(date[6:8])

    url = f"https://www.ejustice.just.fgov.be/cgi_tsv/tsv_l_1.pl?lang=fr&sql=btw+contains+%27{uid}%27&fromtab=TSV&rech=1&pdda=&pddm=&pddj=&pdfa=&pdfm=&pdfj=&naam=&postkode=&localite=&numpu=&hrc=&akte=&btw={uid}&jvorm=&land=&set2=&set3="

    response = requests.get(url)
    soup = bs(response.text,features="lxml").find_all('td')
    for i in range(0, round(len(soup) / 2) - 1):
        test02 = soup[-2 + (-3 * i)].find_all('br')
        test03 = test02[-1].next_sibling
        if date_f in test03:
            result = test02[-1].previous_sibling
            return result

#print(act_obj(687501257, 20180108))