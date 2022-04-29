from pickle import FALSE
import pandas as pd
from math import ceil
from barcode import Code128
from barcode.writer import ImageWriter
from datetime import datetime,date
from PIL import Image, ImageFont, ImageDraw
from PyPDF2 import PdfFileMerger
from os import remove

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
        
    elif code[:-4] not in list(css['Code']) or Name_code not in list(Part_number['Part Num']):
        return_data = {'Error':'Error'}
    return return_data

def update_bill(Supplier:str,Bill_num:str,Bill_date:str,Total_cost:str,Month:str,Year:str):
    df = pd.DataFrame({'Supplier':[Supplier],'Bill num':[Bill_num],'Bill date':[Bill_date],'Total cost':[Total_cost],'Month':[Month],'Year':[Year]})
    df.to_csv('Supplier_Bill.csv', mode='a', encoding='utf-8', index=False, header=False)

def save_css_from_code(code : str, cost : int, sellprice : int, quantity : int):
    #save cost, sell price, stock from code to file
    css = pd.read_csv('Cost_Sellprice_Stock.csv', dtype = str)
    if code[:-4] in css['Code'].to_list():
        row = int(css[css['Code'] == code[:-4]].index.values)
        old_stock = int(css['Stock'][row])
        css.loc[row] = [code[:-4], cost, sellprice, old_stock + quantity]
    elif code[:-4] not in css['Code'].to_list():
        css.loc[len(css['Code'])] = [code[:-4], cost, sellprice, quantity] 
    css.to_csv('Cost_Sellprice_Stock.csv', index=False, encoding='utf-8')

def update_stock_from_code(Code : list, Quantity : list):
    #update already sell item in stock
    css = pd.read_csv('Cost_Sellprice_Stock.csv', dtype = str)
    for c,q in zip(Code,Quantity):
        row = int(css[css['Code'] == c[:-4]].index.values)
        old_stock = int(css['Stock'][row])
        quantity = old_stock - int(q)
        cost = css['Cost'][row]
        sellprice = css['Sellprice'][row]
        css.loc[row] = [c[:-4], cost, sellprice, quantity]
    css.to_csv('Cost_Sellprice_Stock.csv', index=False, encoding='utf-8')


def total_sell_update(All : list):
    sell = int(All[0])
    cost = int(All[1])
    ts = pd.read_csv('Total_sell.csv', dtype=str)
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
    ts.to_csv('Total_sell.csv', index=False, encoding='utf-8')

def create_barcode(code : str, detail : str = '', sellcode : str = ''):
    #gen barcode with code number
    text = get_nsd_from_code(code)[0]+' '+get_nsd_from_code(code)[1]+' '+sellcode+' '+detail
    print(text)
    bar =  Code128(code, writer = ImageWriter())
    bar.save('barcode/' + code, {'module_width':0.35, 'module_height':7, 'font_size':10, 'text_distance':1.2})
    bar = Image.open('barcode/' + code + ".png")
    bar = add_margin(bar,0,0,40,0,(250,250,250))
    bar = add_margin(bar,1,1,1,1,(0,0,0))
    draw = ImageDraw.Draw(bar)
    font = ImageFont.truetype("angsana.ttc",35)
    W, H = bar.size
    draw.text((W/2, 150),text,(0,0,0),font=font, anchor = 'mm')
    bar.save('barcode/' + code + '.png', quality = 300, subsampling=0)

def add_margin(img, top, right, bottom, left, color):
    width, height = img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(img.mode, (new_width, new_height), color)
    result.paste(img, (left,top))
    return result

def sell_price_cal(Cost):
    Sell_Price = ceil(Cost*1.5*(10**-1))*10
    return Sell_Price

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

def sellcode_convert(cost,sell,gen):
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
    
    code = 'K' + sc + 'W' + cc + gen
    return code

def print_barcode_to_pdf(image_name : list, quantity : list):
    page = ceil(sum(quantity)/90)
    nimage = sum(quantity)%90 #store number of image in the last row
    width = 2480 
    height = 3508
    ima = [] #store opened image file
    images = [] #store image that already seperate by row ex.> [image name list of row 1, image name list of row 2]
    x = [] #store list of image that will be appended to images and reset to go to next row
    page_name = [] #store file page pdf name

    for i in range(0,len(image_name)):
        ima += [Image.open(x) for x in ['barcode/' + image_name[i] + '.png']*quantity[i]]

    for p in range(1,page+1):
        if p != page:
            for image in ima[p*90-90:p*90]:
                x += [image]
            images.append(x)
            x = []

        elif p == page:
            for image in ima[-nimage:]:
                x += [image]
            images.append(x)
       
    for i in range(0,page):
        new_im = Image.new('RGB', (width, height), (255,255,255))
        x_offset = 30
        y_offset = 30
        row = ceil(len(images[i])/5)
        nfull = len(images[i])%5

        for y in range(1,row+1):
            if y != row:
                for im in images[i][y*5-5:y*5]:
                    new_im.paste(im, (x_offset, y_offset))
                    x_offset += im.size[0]
                y_offset += im.size[1]
                x_offset = 30
            elif y == row:
                if nfull != 0:
                    for im in images[i][-nfull:]:
                        new_im.paste(im, (x_offset, y_offset))
                        x_offset += im.size[0]
                elif nfull == 0:
                    for im in images[i][-5:]:
                        new_im.paste(im, (x_offset, y_offset))
                        x_offset += im.size[0]

        new_im.save('barcode/page'+ str(i) +'.pdf', 'pdf' ,quality = 300, subsampling=0)
        page_name.append('barcode/page'+ str(i) +'.pdf')

    merge_pdf_page(page_name)

    for i in image_name: #delete barcode image png file
        remove('barcode/' + i + '.png') 
    for x in page_name: # delete pdf page file
        remove(x)


def merge_pdf_page(name_list):

    merger = PdfFileMerger()

    for pdf in name_list:
        merger.append(pdf)

    merger.write('barcode/'+ datetime.now().strftime("%d-%m-%Y"+'_'+'%H-%M-%S') +'.pdf')
    merger.close()

def barcode_check_digit(code_digit_check: str):
    list_code = [int(x) for x in code_digit_check[:-1]]
    odd = sum(list_code[::2])
    even = sum(list_code[1::2])*3
    total = odd+even%10

    if total != 0:
        check_digit = 10-total
    elif total == 0:
        check_digit = 0

    if check_digit == int(code_digit_check[-1]):
        return True
    elif check_digit != int(code_digit_check[-1]):
        return False

def sell(code : list, quantity : list):
    if code and quantity:
        css = pd.read_csv('Cost_Sellprice_Stock.csv', dtype=str)
        
        for i in range(0,len(code)):
            row_num = int(css[css['Code'] == code[i][:-4]].index.values)
            old_stock = int(css['Stock'][row_num])
            if old_stock >= quantity[i]:
                new_stock = old_stock - quantity[i]
                css.loc[row_num,"Stock"]= new_stock
        
        css.to_csv('Cost_Sellprice_Stock.csv', index=False, encoding='utf-8')
            
def main():
    print(get_Code_Number('เฟืองร้อย','PPD','00','00')[:])
    pass
if __name__ == "__main__":
    main()
