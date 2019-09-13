
import pandas as pd
import json
from dictionaries import load_dict
from meta_gen import dict_gen

print('loading tables')

activity = pd.read_csv('./OpenData/activity_f.csv')
table02 = pd.read_csv('./OpenData/address_f.csv')
table03 = pd.read_csv('./OpenData/code.csv')
table04 = pd.read_csv('./OpenData/contact_f.csv')
table05 = pd.read_csv('./OpenData/denomination_f.csv')
table06 = pd.read_csv('./OpenData/enterprise_f.csv')
table07 = pd.read_csv('./OpenData/establishment_f.csv')

print('tables loaded')
#need probably to be re-scraped to match with the pdf's
cie_number = pd.read_json('token.json')

#for testing purpose
cie_number = cie_number[:10]
#formatting TVA number
cie_number[1]= '0'+cie_number[0].astype(str).str[:3]+'.'+cie_number[0].astype(str).str[3:6]+'.'+cie_number[0].astype(str).str[6:9]
EN = cie_number[1].tolist()

print('loading dictionaries')
trad01_jurid_sit,  trad02_type, trad03_jur_form,trad04_nacebel = load_dict()

#EN = ['0923.971.421']
#EN = ['0200.068.636']
#EN = ['0687.533.525']
#EN = ['0200.362.408']


def meta_offset(EN):
    for i in range(0,len(EN)):
        try:
            print(f'traitement {EN[i]}')
            meta_dic = dict_gen(EN[i],activity,table02,table04,table05,table06,table07,trad01_jurid_sit, trad02_type, trad03_jur_form, trad04_nacebel)    
            
            print(meta_dic)        
            with open(f'meta_json/{EN[i]}.json', 'w') as fp:
                json.dump(meta_dic, fp) 
            print('un de plus')
        except:
            print(f'{EN[i]} failed')      
    return('Done')                          

meta_offset(EN)
