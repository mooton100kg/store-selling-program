import pandas as pd

def get_ncss_from_code(code : str):
    #get the name, cost, sell price and stock from code
    Name_code = code[:6]
    css = pd.read_csv('Cost_Sellprice_Stock.csv', dtype = str)
    Part_number = pd.read_csv('Code number/Part number.csv', dtype=str)
    return_data = {'Name':'', 'Cost':'', 'Sellprice':'','Stock':''}
    if code[:-4] in list(css['Code']) and Name_code in list(Part_number['Part Num']):
        row_num = int(css[css['Code'] == code[:-4]].index.values)
        return_data['Name'] = Part_number['Name'][int(Part_number[Part_number['Part Num'] == Name_code].index.values)]

        for i in ['Cost','Sellprice','Stock']:
            return_data[i] = (css[i][row_num])
        

    return return_data

def main():
    pass
if __name__ == "__main__":
    main()
