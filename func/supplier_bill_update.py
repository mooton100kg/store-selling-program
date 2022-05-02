import pandas as pd

def update_bill(Supplier:str,Bill_num:str,Bill_date:str,Total_cost:str,Month:str,Year:str):
    df = pd.DataFrame({'Supplier':[Supplier],'Bill num':[Bill_num],'Bill date':[Bill_date],'Total cost':[Total_cost],'Month':[Month],'Year':[Year]})
    df.to_csv('database/Supplier_Bill.csv', mode='a', encoding='utf-8', index=False, header=False)

