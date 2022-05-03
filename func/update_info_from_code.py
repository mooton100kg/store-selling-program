import pandas as pd
from datetime import date

def update_stock_from_code(Code : list, Quantity : list):
    #update already sell item in stock
    css = pd.read_csv('database/Cost_Sellprice_Stock.csv', dtype = str)

    for c,q in zip(Code,Quantity):
        row = int(css[css['Code'] == c[:-4]].index[0])
        old_stock = int(css['Stock'][row])
        quantity = old_stock - int(q)
        cost = css['Cost'][row]
        sellprice = css['Sellprice'][row]
        css.loc[row] = [c[:-4], cost, sellprice, quantity]

    css.to_csv('database/Cost_Sellprice_Stock.csv', index=False, encoding='utf-8')

def total_sell_update(All : list):
    sell = int(All[0])
    cost = int(All[1])
    ts = pd.read_csv('database/Total_sell.csv', dtype=str)
    m_y = date.today().strftime('%m-%y')
    today = date.today().strftime('%d')
    if m_y in ts['month_year'].to_list():
        row = int(ts[ts['month_year'] == m_y].index.values)
        if today == ts['today'][row]:
            selltoday = int(ts['selltoday'][row]) + sell
            costtoday = int(ts['costtoday'][row]) + cost
            sellyesterday = ts['sellyesterday'][row]
            costyesterday = ts['costyesterday'][row]
        elif today != ts['today'][row]:
            selltoday = sell
            costtoday = cost
            if int(ts['today'][row]) == int(today)-1:
                sellyesterday = ts['selltoday'][row]
                costyesterday = ts['costtoday'][row]
            elif int(ts['today'][row]) != int(today)-1:
                sellyesterday = 0
                costyesterday = 0
        sellallmonth = int(ts['sellallmonth'][row]) + sell
        costallmonth = int(ts['costallmonth'][row]) + cost
    elif m_y not in ts['month_year'].to_list():
        row = len(ts['month_year'])
        sellyesterday = 0
        costyesterday = 0
        sellallmonth = sell
        costallmonth = cost
        selltoday = sell
        costtoday = cost
    ts.loc[row] = [today, costtoday, selltoday, costyesterday, sellyesterday, costallmonth, sellallmonth, m_y]
    ts.to_csv('database/Total_sell.csv', index=False, encoding='utf-8')

def sell(code : list, quantity : list):
    if code and quantity:
        css = pd.read_csv('database/Cost_Sellprice_Stock.csv', dtype=str)
        
        for i in range(0,len(code)):
            row_num = int(css[css['Code'] == code[i][:-4]].index.values)
            old_stock = int(css['Stock'][row_num])
            if old_stock >= quantity[i]:
                new_stock = old_stock - quantity[i]
                css.loc[row_num,"Stock"]= new_stock
        
        css.to_csv('database/Cost_Sellprice_Stock.csv', index=False, encoding='utf-8')

def save_css_from_code(code : str, cost : int, sellprice : int, quantity : int):
    #save cost, sell price, stock from code to file     +    save restock alert
    css = pd.read_csv('database/Cost_Sellprice_Stock.csv', dtype = str)
    ra = pd.read_csv('database/Restock_Alert.csv', dtype=str)

    if code[:-4] in css['Code'].to_list():
        row = css[css['Code'] == code[:-4]].index[0]
        old_stock = int(css['Stock'][row])
        css.loc[row] = [code[:-4], cost, sellprice, old_stock + quantity]

        row = ra[ra['Code'] == code[:-4]].index[0]
        old_min = ra['Minimum'][row]
        ra.loc[row] = [code[:-4], old_min,'0'] 
    elif code[:-4] not in css['Code'].to_list():
        css.loc[len(css['Code'])] = [code[:-4], cost, sellprice, quantity] 
        ra.loc[len(ra['Minimum'])] = [code[:-4], '1','0'] 
        
    css.to_csv('database/Cost_Sellprice_Stock.csv', index=False, encoding='utf-8')
    ra.to_csv('database/Restock_Alert.csv', index=False, encoding='utf-8')