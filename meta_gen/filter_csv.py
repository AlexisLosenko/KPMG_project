import pandas as pd

token = pd.read_json('token.json')
token.drop_duplicates(inplace=True)
token[0].tolist()

print('loading tables')

activity = pd.read_csv('./OpenData/activity.csv')
table02 = pd.read_csv('./OpenData/address.csv')
table03 = pd.read_csv('./OpenData/code.csv')
table04 = pd.read_csv('./OpenData/contact.csv')
table05 = pd.read_csv('./OpenData/denomination.csv')
table06 = pd.read_csv('./OpenData/enterprise.csv')
table07 = pd.read_csv('./OpenData/establishment.csv')

activity = activity[activity[]]

