from pymongo import MongoClient
import pandas as pd
import json
from dictionaries import load_dict
from meta_gen import dict_gen

print('loading tables')

activity = pd.read_csv('./OpenData/activity.csv')
table02 = pd.read_csv('./OpenData/address.csv')
table03 = pd.read_csv('./OpenData/code.csv')
table04 = pd.read_csv('./OpenData/contact.csv')
table05 = pd.read_csv('./OpenData/denomination.csv')
table06 = pd.read_csv('./OpenData/enterprise.csv')
table07 = pd.read_csv('./OpenData/establishment.csv')

print('tables loaded')
#need probably to be re-scraped to match with the pdf's
vat_numbers = pd.read_json('token.json')

#TODO for testing purpose - remove
vat_numbers = vat_numbers[:10]

vat_numbers = "0" + vat_numbers.astype(str)
#formatting TVA number
vat_numbers[1]= vat_numbers[0].str[:3] + '.' + vat_numbers[0].str[3:6] + \
                '.'+vat_numbers[0].str[6:9]
vat_uids = vat_numbers[0].tolist()
vat_formatted = vat_numbers[1].tolist()

print(vat_uids)
print(vat_formatted)


print('loading dictionaries')
trad01_jurid_sit,  trad02_type, trad03_jur_form,trad04_nacebel = load_dict()


def update_statutes_in_db(uids):
    client = MongoClient()
    db = client.kpmg
    stat_coll = db.statutes
    for uid in uids :
        stat_doc = stat_coll.find_one({"_id": uid})
        if stat_doc :
            meta_dic = dict_gen(uid, activity, table02, table04, table05, table06, table07, trad01_jurid_sit,
                                trad02_type, trad03_jur_form, trad04_nacebel)
            print(meta_dic)
            #TODO update db code here instead of print
        else :
            print("Document with uid " + str(uid) + " not found in database")


update_statutes_in_db(vat_uids)
