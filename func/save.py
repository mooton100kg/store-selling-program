import shutil,os
from datetime import datetime


def Save():
    save_file = 'C:/Users/pk/Desktop/auto_save/' + datetime.now().strftime('%d-%m-%Y__%H-%M-%S')

    if not os.path.exists(r'C:\Users\pk\Desktop\auto_save'):
        os.makedirs(r'C:\Users\pk\Desktop\auto_save')

    if not os.path.exists(save_file):
        os.makedirs(save_file)

    shutil.copytree('Code number', f'{save_file}/Code number', copy_function = shutil.copy) 
    shutil.copytree('database', f'{save_file}/database', copy_function = shutil.copy) 

def Load(folder: str):

    if len(os.listdir(folder)) == 2:
        Save()
        shutil.rmtree('Code number')
        shutil.rmtree('database')
        shutil.copytree(folder+r'\Code number','Code number', copy_function = shutil.copy)
        shutil.copytree(folder+r'\database','database', copy_function = shutil.copy)




