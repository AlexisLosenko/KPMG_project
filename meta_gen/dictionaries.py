def load_dict(table03):
    trad = table03[['Category', 'Code', 'Description']][table03.Language == 'FR']
    dict_list = []
    for cat in trad.Category.unique():
        temp_trad = trad[trad.Category == cat]
        keys = temp_trad['Code'].to_list()
        values = temp_trad['Description'].to_list()
        dict_list.append(dict(zip(keys, values)))

    ActivityGroup_dic = dict_list[0]
    # Classification_dic = dict_list[1]
    # ContactType_dic = dict_list[2]
    # EntityContact_dic = dict_list[3]
    JuridicalForm_dic = dict_list[4]
    JuridicalSituation_dic = dict_list[5]
    # Language_dic = dict_list[6]
    Nace2003_dic = dict_list[7]
    Nace2008_dic = dict_list[8]
    #Status_dic = dict_list[9]
    # TypeOfAddress_dic = dict_list[10]
    # TypeOfDenomination_dic = dict_list[11]
    TypeOfEnterprise_dic = dict_list[12]
    return ActivityGroup_dic,  JuridicalForm_dic, JuridicalSituation_dic,\
           Nace2003_dic, Nace2008_dic, TypeOfEnterprise_dic