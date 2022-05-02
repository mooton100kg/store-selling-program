from math import ceil

def sell_price_cal(Cost):
    Sell_Price = ceil(Cost*1.5*(10**-1))*10
    return Sell_Price

def sellcode_convert(cost:str,sell:str):
    sell_code = ('S','R','Y','Z','M','L','H','G','P','J')
    Cost_code = ('N','E','D','I','X','A','F','O','C','B')
    sc = ''
    s = [int(i) for i in str(sell)]
    for i in s:
        sc += sell_code[i-1]
    cc = ''
    c = [int(i) for i in str(cost)]
    for i in c:
        cc += Cost_code[i-1]
    
    code = 'K' + sc + 'W' + cc
    return code