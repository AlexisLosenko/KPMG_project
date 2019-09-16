import pandas as pd
def dict_gen(element,activity,table02,table04,table05,table06,table07,
             ActivityGroup_dic,  JuridicalForm_dic, JuridicalSituation_dic, Nace2003_dic, Nace2008_dic,  TypeOfEnterprise_dic):

    meta_dic = dict()

    # formatting 2 features from table 06 to match with the code table (table03)
    temp = table06.JuridicalForm.fillna(0).astype(int).astype(str)
    temp2 = table06.JuridicalSituation.fillna(0).astype(int).astype(str)
    temp = ["0" + i if len(i) == 2 else "00" + i if len(i) == 1 else i for i in temp]
    temp2 = ["0" + i if len(i) == 2 else "00" + i if len(i) == 1 else i for i in temp2]
    table06.JuridicalForm = temp
    table06.JuridicalSituation = temp2

    table06_row = table06[table06['EnterpriseNumber'] == element]
    table05_row = table05[table05['EntityNumber'] == element]
    table05_row_abbr = table05[(table05['EntityNumber'] == element) & (table05.TypeOfDenomination == 2)]
    table01_row_main = activity[(activity['EntityNumber'] == element) & (activity.Classification == 'MAIN')].astype(str)
    table01_row_sec = activity[(activity['EntityNumber'] == element) & (activity.Classification == 'SECO')]
    table07_row = table07[table07['EnterpriseNumber'] == element]
    table02_row = table02[table02['EntityNumber'] == element]
    table04_row_mail = table04[(table04['EntityNumber'] == element) & (table04['ContactType'] == 'EMAIL')]
    table04_row_phone = table04[(table04['EntityNumber'] == element) & (table04['ContactType'] == 'TEL')]

    if len(table06_row) == 0:
        print('not in the csv')
    else:
        meta_dic['VAT Number'] = table06_row.iloc[0]['EnterpriseNumber']

        meta_dic['Denomination'] = table05_row.iloc[0]['Denomination']

        meta_dic['Abbr'] = (lambda x: table05_row_abbr.iloc[0]['Denomination']
        if len(table05_row_abbr) != 0 else 'NONE')(element)

        meta_dic['ActivityGroup'] = (lambda x: table01_row_main.iloc[0]['ActivityGroup']
        if len(table01_row_main) != 0 else "none")(element)

        meta_dic['Main activity'] = (
            lambda x: [table01_row_main.iloc[0]['NaceVersion'], table01_row_main['NaceCode'].unique().tolist()]
            if len(table01_row_main) != 0 else "none")(element)

        meta_dic['Secondary activity'] = (lambda x: table01_row_sec['NaceCode'].unique().tolist()
        if len(table01_row_sec) != 0 else "none")(element)

        meta_dic['Foundation Date'] = table06_row['StartDate'].iloc[0]

        meta_dic['Establishment #'] = len(table07_row)

        meta_dic['Establishment StartDate'] = table07_row['StartDate'].to_list()

        meta_dic['JuridicalSituation'] = str(table06_row.iloc[0]['JuridicalSituation'])

        meta_dic['TypeOfEnterprise'] = str(table06_row.iloc[0]['TypeOfEnterprise'])

        meta_dic['JuridicalForm'] = str(table06_row.iloc[0]['JuridicalForm'])

        # meta_dic['Language']= table06_row.iloc[0]['TypeOfEnterprise']

        meta_dic['Zipcode'] = table02_row.iloc[0]['Zipcode']

        meta_dic['Street'] = table02_row.iloc[0]['StreetFR']

        meta_dic['HouseNumber'] = table02_row.iloc[0]['HouseNumber']

        meta_dic['Mail'] = (lambda x: table04_row_mail.iloc[0]['Value']
        if len(table04_row_mail) != 0 else 'NA')(element)

        meta_dic['Phone'] = (lambda x: table04_row_phone.iloc[0]['Value']
        if len(table04_row_phone) != 0 else 'NA')(element)

        for KEY, VALUE in ActivityGroup_dic.items():
            if meta_dic['ActivityGroup'] == KEY:
                meta_dic['ActivityGroup'] = VALUE

        for KEY, VALUE in JuridicalForm_dic.items():
            if meta_dic['JuridicalForm'] == KEY:
                meta_dic['JuridicalForm'] = VALUE

        for KEY, VALUE in JuridicalSituation_dic.items():
            if meta_dic['JuridicalSituation'] == KEY:
                meta_dic['JuridicalSituation'] = VALUE

        for KEY, VALUE in TypeOfEnterprise_dic.items():
            if meta_dic['TypeOfEnterprise'] == KEY:
                meta_dic['TypeOfEnterprise'] = VALUE

        if meta_dic['Main activity'][0] == 2003:
            for KEY, VALUE in Nace2003_dic.items():
                for i in range(0, len(meta_dic['Main activity'])):
                    if meta_dic['Main activity'][1][i] == KEY:
                        meta_dic['Main activity'][1][i] = (KEY, VALUE)

            for i in range(0, len(meta_dic['Secondary activity'])):
                if meta_dic['Secondary activity'][i] == KEY:
                    meta_dic['Secondary activity'][i] = (KEY, VALUE)
        else:
            for KEY, VALUE in Nace2008_dic.items():
                for i in range(0, len(meta_dic['Main activity'][1])):
                    if meta_dic['Main activity'][1][i] == KEY:
                        meta_dic['Main activity'][1][i] = (KEY, VALUE)

            for i in range(0, len(meta_dic['Secondary activity'])):
                if meta_dic['Secondary activity'][i] == KEY:
                    meta_dic['Secondary activity'][i] = (KEY, VALUE)
    return(meta_dic)
