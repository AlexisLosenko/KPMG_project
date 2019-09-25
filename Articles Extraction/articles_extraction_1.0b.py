from pymongo import MongoClient
import json
#from googletrans import Translator
from json.decoder import JSONDecodeError
import translators
#translator = Translator()

client = MongoClient()
db = client.kpmg
stat_coll = db.statutes

# key word to be found in the text:
key_word = ["Art", "Article", 'Art.', 'Art,', 'Ast', 'Ari', "art", "At", "ARTICLE", "ART", 'Ant', 'Artikel', 'ARTIKEL',
            'article', 'Articdle']
# VAT number list
filename = r'C:\Users\sebch\Desktop\kpmg\GitHub Repo\KPMG_project\scraping_final\scraping_staatblad_seb\token_test.json'
with open(filename, 'r') as f:
    uids = json.load(f)

uids= uids[:10]

log = []
log_trad_art = []
log_trad_full = []

for uid in uids:
    try:
        # fetching cie first document data
        print(f'trying {uid}')
        stat_doc = stat_coll.find_one({"_id": uid})
        doc_data = stat_doc['documents']
        date = [i for i in doc_data][0]
        lang = stat_doc['language']

        # checking if it is a consitution doc
        obje = doc_data[date]['object']
        constitution = ['CONSTITUTION', 'OPRICHTING', 'STATUTS', 'STATUTEN']
        for obj in obje.split():
            if obj in constitution:

                # look for key_word in text splited
                text = next(iter(next(iter(doc_data.values())).values()))

                # split the text by "lignes"
                split = text.split('\n')
                # index of each ligne containing one the key_word
                cut_index = []
                for group in split:
                    # removing useless characters and splitting by 'words'
                    for word in group.translate({ord(i): ' ' for i in ":[‘'(),. "}).split():
                        if word in key_word:
                            cut_index.append(split.index(group))

                # text until first occurence of on e key_word
                start = split[:cut_index[0] - 1]
                # between two occurences
                articles = []
                for i in cut_index:
                    if i != cut_index[-1]:
                        articles.append(split[i:cut_index[cut_index.index(i) + 1]])
                # after the last occurences
                end = split[cut_index[-1] + 1:]

                sections = [start] + articles + [end]
                # avoiding list of several string (need to be fine tuned)
                for element in sections:
                    temp = str()
                    for el in element:
                        temp += el

                    sections[sections.index(element)] = temp

                # injection in the db
                stat_coll.update_one({'_id': uid},
                                     {'$addToSet': {
                                         f"documents.{date}.sections": {str(sections.index(element)): element for
                                                                        element in
                                                                        sections}
                                     }},
                                     upsert=True
                                     )


                log.append(uid)
                print(f'added {uid}')

                # translate the full text and add to the db

                try:
                     translation = translators.google(text=text[:4999],
                                        from_language=lang,
                                        to_language='en',
                                        host='https://translate.google.be',
                                        is_detail=False,
                                        proxy=None)
                     stat_coll.update_one({'_id': uid},
                                          {'$set':
                                               {f"documents.{date}.translation": translation}
                                           },
                                          upsert=True
                                          )
                     print("traduction added")
                     log_trad_full.append([uid, len(text)])
                except JSONDecodeError:

                     print('unable to translate text')
                # translation articles by articles
                try:


                    sections_t = [translators.google(text=i[:4999],
                                       from_language=lang,
                                       to_language='en',
                                       host='https://translate.google.be',
                                       is_detail=False,
                                       proxy=None) for i in sections]
                    print(sections_t)
                    stat_coll.update_one({'_id': uid},
                                         {'$addToSet': {
                                             f"documents.{date}.sections": {str(sections_t.index(element)): element for
                                                                            element in
                                                                            sections_t}
                                         }},
                                         upsert=True
                                         )
                    log_trad_art.append(uid)
                except JSONDecodeError:
                    print('unable to translate articles')


            else:
                pass
    except TypeError:
        print(f'no document found for {uid}')
    except IndexError:
        print(f'cannot parse document for {uid}')
    except AttributeError:
        print(f'cannot find document object for {uid}')

with open('log.json', 'w', encoding='utf-8') as g:
    json.dump(log, g, ensure_ascii=False, indent=4)

with open('log_trad_full.json', 'w', encoding='utf-8') as g:
    json.dump(log_trad_full, g, ensure_ascii=False, indent=4)

with open('log_trad_art.json', 'w', encoding='utf-8') as g:
    json.dump(log_trad_art, g, ensure_ascii=False, indent=4)