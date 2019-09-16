import wget
import time
import requests
from fake_useragent import UserAgent


start = 45000
amount = 200
base_url = "http://statuten.notaris.be/costa_v1/api/costa-api/documents/"
#base_url = "https://plop.n8e.be/pdf/"

###change this line###
dl_dir = '/home/sebchko/Desktop/KPMG/pdf2/'
###realy###
sleep_time = 0.5
ua = UserAgent()


for i in range(amount):
    pos = start + i
    url = base_url + str(pos)
    dl_file = dl_dir + str(pos) + '.pdf'

    myfile = requests.get(url, headers={'User-Agent': ua.random}, verify=False)
    with open(f'{dl_file}', 'wb') as file:
        file.write(myfile.content) 

    #wget.download(url, dl_file)
    #print(f"download {url} to {dl_file}")
    time.sleep(sleep_time)