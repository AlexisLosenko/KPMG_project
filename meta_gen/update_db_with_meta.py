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
vat_numbers = vat_numbers[:50]

vat_numbers = "0" + vat_numbers.astype(str)
##formatting TVA number not needed here anymore
#vat_numbers[1]= vat_numbers[0].str[:4] + '.' + vat_numbers[0].str[4:7] + \
                '.'+vat_numbers[0].str[7:10]
vat_uids = vat_numbers[0].tolist()
#vat_formatted = vat_numbers[1].tolist()

print(vat_uids)
#print(vat_formatted)


print('loading dictionaries')
ActivityGroup_dic,  JuridicalForm_dic, JuridicalSituation_dic, Nace2003_dic, Nace2008_dic,TypeOfEnterprise_dic = load_dict(table03)


def update_statutes_in_db(uids):
    client = MongoClient()
    db = client.kpmg
    stat_coll = db.statutes
    for uid in uids :
        stat_doc = stat_coll.find_one({"_id": uid})
        if stat_doc :
            meta_dic = dict_gen(uid, activity, table02, table04, table05, table06, table07,
                ActivityGroup_dic,  JuridicalForm_dic, JuridicalSituation_dic, Nace2003_dic, Nace2008_dic, TypeOfEnterprise_dic )
            meta_dic.update(stat_doc) #this way fields in stat_doc do not get overwritten
            stat_coll.update_one({'_id': uid}, {"$set": meta_dic}, upsert=False)
            print("Found statute with uid " + uid + ". Updated meta data where empty")

        else :
            print("Document with uid " + str(uid) + " not found in database")


update_statutes_in_db(vat_uids)
