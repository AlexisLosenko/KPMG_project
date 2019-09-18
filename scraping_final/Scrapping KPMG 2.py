import wget
import pandas as pd
import time
import sys
import os 
import json
import pandas as pd 

#On importe les liens contenus dans le ficher json avec pandas
df=pd.read_json(r'link_each_entreprise.json')
print(df)

#On change la df en liste
for index, url in df.items():
    df1=list(url)
   
#Avec BeautifulSoup on extrait les liens pdf pour les sauver dans un fichier json
annuaire_pdf=[]

for url in df1:
    html_page = urlopen(url)
    soup = BeautifulSoup(html_page)
    for link in soup.findAll('a', attrs={'href': re.compile("pdf$")}):
        link_pdf= link.get('href')
        print(link_pdf)
        
        annuaire_pdf.append(link_pdf)
        
        with open('lien_pdf.json', 'w', encoding='utf-8') as f:
            json.dump(annuaire_pdf, f, ensure_ascii=False, indent=4)

#On télécharge les pdfs depuis les liens grace à wget 
#On importe les liens des pdf:
dfpdf=pd.read_json('lien_pdf.json')
dfpdf=dfpdf.drop_duplicates()

#On transforme le df en une liste
for index, url in dfpdf.items():
    df1pdf=list(url)
   
for link in df1pdf: 
    try:
        print(f'trying: {link}')
        pdfname = link[-12:]
        
        #Permet de vérifier si le fichir existe déjà et ne pas créer de doublons
        if os.path.exists('./pdf/'+ str(pdfname)) is False:
            wget.download(link, r'C:\Users\Pierro\Documents\pdf')
            time.sleep(0.2)
        else:
            pass

    except:
        print(f'ERROR url: {link}')
        print(sys.exc_info())  
        
                
        
# Si on ne créer pas l'exeption on a l'erreur:
#       ConnectionResetError: [WinError 10054] Une connexion existante a dû être fermée par l’hôte distant      