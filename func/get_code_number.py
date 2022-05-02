import pandas as pd

def get_Code_Number(Name : str , Supplier : str, month : str , year : str):
    Part_number = pd.read_csv('Code number\Part number.csv', dtype=str)
    Supplier_number = pd.read_csv('Code number\Supplier number.csv', dtype=str)
    S = Supplier in list(Supplier_number['Supplier'])
    N = Name in list(Part_number['Name'])

    if S == False and N == False:
        Name_code = str(len(Part_number['Name'])).zfill(6)
        Supplier_code = str(len(Supplier_number['Supplier'])).zfill(2)
        Part_number.loc[len(Part_number.index)] = Name_code,Name
        Supplier_number.loc[len(Supplier_number.index)] = Supplier_code,Supplier
    elif S == False and N == True:
        Name_code = Part_number['Part Num'][int(Part_number[Part_number['Name'] == Name].index.values)]
        Supplier_code = str(len(Supplier_number['Supplier'])).zfill(2)
        Supplier_number.loc[len(Supplier_number.index)] = Supplier_code,Supplier
    elif S == True and N == False:
        Name_code = str(len(Part_number['Name'])).zfill(6)
        Supplier_code = Supplier_number['Supplier Num'][int(Supplier_number[Supplier_number['Supplier'] == Supplier].index.values)]
        Part_number.loc[len(Part_number.index)] = Name_code,Name
    else:
        Name_code = Part_number['Part Num'][int(Part_number[Part_number['Name'] == Name].index.values)]
        Supplier_code = Supplier_number['Supplier Num'][int(Supplier_number[Supplier_number['Supplier'] == Supplier].index.values)]

    Part_number.to_csv('Code number\Part number.csv', index=False, encoding='utf-8')
    Supplier_number.to_csv('Code number\Supplier number.csv', index=False, encoding='utf-8')

    return Name_code + Supplier_code + month + year