import pandas as pd

def get_ncss_from_code(code : str):
    #get the name, cost, sell price and stock from code
    Name_code = code[:6]
    css = pd.read_csv('database/Cost_Sellprice_Stock.csv', dtype = str)
    Part_number = pd.read_csv('Code number/Part number.csv', dtype=str)
    return_data = {'Name':'', 'Cost':'', 'Sellprice':'','Stock':''}
    if code[:-4] in list(css['Code']) and Name_code in list(Part_number['Part Num']):
        row_num = int(css[css['Code'] == code[:-4]].index.values)
        return_data['Name'] = Part_number['Name'][int(Part_number[Part_number['Part Num'] == Name_code].index.values)]

        for i in ['Cost','Sellprice','Stock']:
            return_data[i] = (css[i][row_num])
        
    elif code[:-4] not in list(css['Code']) or Name_code not in list(Part_number['Part Num']):
        return_data = {'Error':'Error'}
    return return_data

def get_nsd_from_code(code : str):
    #get name, supplier from code 
    Name_code = code[:6]
    Supplier_code = code[6:8]
    Part_number = pd.read_csv('Code number/Part number.csv', dtype=str)
    Supplier_number = pd.read_csv('Code number/Supplier number.csv', dtype=str)
    return_data = []

    if Name_code in list(Part_number['Part Num']) and Supplier_code in list(Supplier_number['Supplier Num']):
            return_data.append(Part_number['Name'][int(Part_number[Part_number['Part Num'] == Name_code].index.values)])
            return_data.append(Supplier_number['Supplier'][int(Supplier_number[Supplier_number['Supplier Num'] == Supplier_code].index.values)])

    return return_data

    