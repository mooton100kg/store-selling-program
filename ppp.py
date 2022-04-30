import pandas as pd
x = pd.read_csv('Cost_Sellprice_Stock.csv',dtype=str)
if '00000019' in list(x['Code']):
    print('hello')