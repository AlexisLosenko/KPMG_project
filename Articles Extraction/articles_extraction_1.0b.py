from pymongo import MongoClient
import json


client = MongoClient()
db = client.kpmg
stat_coll = db.statutes


key_word = ["Art", "Article", 'Art.', 'Art,', 'Ast', 'Ari', "art", "At", "ARTICLE", "ART", 'Ant', 'Artikel', 'ARTIKEL' , 'article']

filename = r'C:\Users\sebch\Desktop\kpmg\GitHub Repo\KPMG_project\scraping_final\scraping_staatblad_seb\token_2018.json'
with open(filename, 'r') as f:
    uids = json.load(f)


for uid in uids:
    try:
        # fetching cie first document data
        print(f'trying {uid}')
        stat_doc = stat_coll.find_one({"_id": uid})
        doc_data = stat_doc['documents']
        date = [i for i in doc_data][0]

        #checking if it is a consitution doc
        obje = doc_data[date]['object']
        constitution = ['CONSTITUTION', 'OPRICHTING', 'STATUTS', 'STATUTEN']
        for obj in obje.split():
            if obj in constitution:

                #look for key_word in text splitted
                text = next(iter(next(iter(doc_data.values())).values()))
                split = text.split('\n')
                #index of each ligne containing one the key_word
                cut_index = []
                for group in split:
                    #removing useless characters and splitting byt 'words'
                    for word in group.translate({ord(i): ' ' for i in ":[‘'(),. "}).split():
                        if word in key_word:
                            cut_index.append(split.index(group))

                start = split[:cut_index[0] - 1]

                articles = []
                for i in cut_index:
                    if i != cut_index[-1]:
                        articles.append(split[i:cut_index[cut_index.index(i) + 1]])

                end = split[cut_index[-1] + 1:]

                sections = [start] + articles + [end]

                for element in sections:
                    temp = str()
                    for el in element:
                        temp += el

                    sections[sections.index(element)] = temp

                stat_coll.update_one({'_id': uid},
                                     {'$addToSet': {
                                         f"documents.{date}.sections": {str(sections.index(element)): element for element in
                                                                        sections}
                                     }},
                                     upsert=True
                                     )
                print(f'added {uid}')
            else :
                pass
    except TypeError:
        print(f'no document found for {uid}')
    except IndexError:
        print(f'cannot parse document for {uid}')
    except AttributeError:
        print(f'cannot find document object for {uid}')