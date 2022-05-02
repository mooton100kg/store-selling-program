from PIL import Image, ImageFont, ImageDraw
from PyPDF2 import PdfFileMerger
from os import remove
from barcode import Code128
from barcode.writer import ImageWriter
from math import ceil
from datetime import datetime

from func import get_nsd_from_code

def create_barcode(code : str, detail : str = '', sellcode : str = ''):
    #gen barcode with code number
    text = get_nsd_from_code(code)[0]+' '+get_nsd_from_code(code)[1]+' '+sellcode+' '+detail
    bar =  Code128(code, writer = ImageWriter())
    bar.save('barcode/' + code, {'module_width':0.35, 'module_height':7, 'font_size':10, 'text_distance':1.2})
    bar = Image.open('barcode/' + code + ".png")
    bar = add_margin(bar,0,0,40,0,(255,255,255))
    bar = add_margin(bar,1,1,1,1,(0,0,0))
    draw = ImageDraw.Draw(bar)
    font = ImageFont.truetype("font/angsana.ttc",35)
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