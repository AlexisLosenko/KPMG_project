import pandas as pd
def dict_gen(element,activity,table02,table04,table05,table06,table07,trad01_jurid_sit, trad02_type, trad03_jur_form, trad04_nacebel):

    table07group = table07.groupby('EnterpriseNumber').count()
#            table07group.StartDate[table07group.index == element]

    meta_dic = dict()

    meta_dic['VAT Number']=  table06['EnterpriseNumber'][table06['EnterpriseNumber']== element].tolist()[0] 

    meta_dic['Denomination'] = table05['Denomination'][(table05['EntityNumber'] == element)].tolist()[0]

#meta_dic['Abbr'] = table05['Denomination'][(table05['EntityNumber'] == element)].tolist()[1]

    meta_dic['Abbr'] = (lambda x: table05['Denomination'][(table05['EntityNumber'] == x)&(table05.TypeOfDenomination == 2)].tolist() 
        if len(table05['Denomination'][(table05['EntityNumber'] == x)&(table05.TypeOfDenomination == 2)].tolist()) != 0 
        else 'NONE')(element)

    meta_dic['Main activity'] = activity['NaceCode'][(activity.EntityNumber == element)&(activity.Classification == 'MAIN')].to_list()

    meta_dic['Secondary activity'] = (lambda x: activity['NaceCode'][(activity.EntityNumber == x)&(activity.Classification == 'SECO')].tolist() 
        if len(activity['NaceCode'][(activity.EntityNumber == x)&(activity.Classification == 'SECO')].tolist()) != 0 else 'NONE')(element)

    meta_dic['Foundation Date']=table06['StartDate'][table06['EnterpriseNumber']== element].tolist()[0]

    meta_dic['Establishment #'] = (lambda x: int(table07group.StartDate[table07group.index == x]) 
        if len(pd.Series(table07group.index == x).unique())== 2  else 0)(element)

    meta_dic['Establishment StartDate'] = table07['StartDate'][table07['EnterpriseNumber']==element].to_list()

    meta_dic['JuridicalSituation']= int(table06['JuridicalSituation'][table06['EnterpriseNumber']==element])

    meta_dic['TypeOfEnterprise']=int(table06['TypeOfEnterprise'][table06['EnterpriseNumber']==element])

    meta_dic['JuridicalForm']=int(table06['JuridicalForm'][table06['EnterpriseNumber']==element])

#meta_dic['Language']=int(table06['TypeOfEnterprise'][table06['EnterpriseNumber']==EN[0]])

    meta_dic['Zipcode'] = int(table02['Zipcode'][table02['EntityNumber'] == element])

    meta_dic['Street'] = table02['StreetFR'][table02['EntityNumber'] == element].tolist()[0]

    meta_dic['HouseNumber'] = table02['HouseNumber'][table02['EntityNumber'] == element].astype(str).tolist()[0]

    meta_dic['Mail'] = (lambda x: table04['Value'][(table04['EntityNumber']==x) &(table04['ContactType']== 'EMAIL')].tolist()[0] 
        if len(table04['Value'][(table04['EntityNumber'] == x)&(table04['ContactType']== 'EMAIL')].tolist()) != 0  else 'NA')(element)

    meta_dic['Phone'] = (lambda x: table04['Value'][(table04['EntityNumber']==x) &(table04['ContactType']== 'TEL')].tolist()[0] 
        if len(table04['Value'][(table04['EntityNumber'] == x)&(table04['ContactType']== 'TEL')].tolist()) != 0  else 'NA')(element)


    for key, value in meta_dic.items():
        for KEY, VALUE in trad01_jurid_sit.items():
            if meta_dic['JuridicalSituation'] == KEY:
                meta_dic['JuridicalSituation'] = VALUE
        for KEY, VALUE in trad02_type.items():
            if meta_dic['TypeOfEnterprise'] == KEY:
                meta_dic['TypeOfEnterprise'] = VALUE            
        for KEY, VALUE in trad03_jur_form.items():
            if meta_dic['JuridicalForm'] == KEY:
                meta_dic['JuridicalForm'] = VALUE
        for KEY, VALUE in trad04_nacebel.items():
            for i in range (0,len(meta_dic['Main activity'])):
                if meta_dic['Main activity'][i] == KEY:
                    meta_dic['Main activity'][i] = (KEY,VALUE)
        for KEY, VALUE in trad04_nacebel.items():
            for i in range (0,len(meta_dic['Secondary activity'])):
                if meta_dic['Secondary activity'][i] == KEY:
                    meta_dic['Secondary activity'][i] = (KEY,VALUE)
    return(meta_dic)
