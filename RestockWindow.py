from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import pandas as pd
from datetime import date
from main import sell_price_cal, get_Code_Number, save_css_from_code, create_barcode, print_barcode_to_pdf

class Restock_Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Restock_Window, self).__init__()
        self.font = QtGui.QFont()
        self.font.setPointSize(16)
        self.css_file = pd.read_csv('Cost_Sellprice_Stock.csv', dtype=str)
        self.Part_number = pd.read_csv('Code number/Part number.csv', dtype=str)
        self.Supplier_number = pd.read_csv('Code number/Supplier number.csv', dtype=str)
        self.input_info = {'Name':[],'Supplier':[],'Cost':[],'Sell price':[],'Month':[],'Year':[],'Quantity':[]}
        self.setupUi()

    def setupUi(self):
        self.resize(594, 522)
        self.gridLayoutWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.gridLayoutWidget)
        self.main_gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        
        #sub grideLayout
        self.input_gridLayout = QtWidgets.QGridLayout()
        self.main_gridLayout.addLayout(self.input_gridLayout, 0,1,1,1)


        #Name
        self.Name_Label = QtWidgets.QLabel('Name :')
        self.Name_Label.setFont(self.font)
        self.Name_Label.setAlignment(QtCore.Qt.AlignRight)
        self.Name_Label.setFixedWidth(100)
        self.input_gridLayout.addWidget(self.Name_Label, 0, 0, 1, 1)

        self.Name_LineEdit = QtWidgets.QLineEdit()
        self.Name_LineEdit.setFont(self.font)
        self.Name_LineEdit.setFixedWidth(150)
        self.Name_LineEdit.editingFinished.connect(lambda: self.Supplier_LineEdit.setFocus())
        self.Name_LineEdit.setCompleter(QtWidgets.QCompleter(self.Part_number['Name'].to_list()))
        self.input_gridLayout.addWidget(self.Name_LineEdit, 0, 1, 1, 1)
        #-------------------------------------------------------------

        #Supplier
        self.Supplier_Label = QtWidgets.QLabel('Supplier :')
        self.Supplier_Label.setFont(self.font)
        self.Supplier_Label.setAlignment(QtCore.Qt.AlignRight)
        self.Supplier_Label.setFixedWidth(100)
        self.input_gridLayout.addWidget(self.Supplier_Label, 1, 0, 1, 1)

        self.Supplier_LineEdit = QtWidgets.QLineEdit()
        self.Supplier_LineEdit.setFont(self.font)
        self.Supplier_LineEdit.setFixedWidth(150)
        self.Supplier_LineEdit.editingFinished.connect(lambda: self.SupplierName_LineEdit_Finish())
        self.Supplier_LineEdit.setCompleter(QtWidgets.QCompleter(self.Supplier_number['Supplier'].to_list()))
        self.input_gridLayout.addWidget(self.Supplier_LineEdit, 1, 1, 1, 1)
        #------------------------------------------------------------

        #Cost
        self.Cost_Label = QtWidgets.QLabel('Cost :')
        self.Cost_Label.setFont(self.font)
        self.Cost_Label.setAlignment(QtCore.Qt.AlignRight)
        self.Cost_Label.setFixedWidth(100)
        self.input_gridLayout.addWidget(self.Cost_Label, 2, 0, 1, 1)

        self.Cost_LineEdit = QtWidgets.QLineEdit()
        self.Cost_LineEdit.setFont(self.font)
        self.Cost_LineEdit.setFixedWidth(150)
        self.Cost_LineEdit.setToolTip('Add + to auto calculate sell price')
        self.Cost_LineEdit.editingFinished.connect(lambda: self.Cost_LineEdit_Finish())
        self.input_gridLayout.addWidget(self.Cost_LineEdit, 2, 1, 1, 1)
        #-------------------------------------------------------------

        #Sell price
        self.Sellprice_Label = QtWidgets.QLabel('Sell price :')
        self.Sellprice_Label.setFont(self.font)
        self.Sellprice_Label.setAlignment(QtCore.Qt.AlignRight)
        self.Sellprice_Label.setFixedWidth(100)
        self.input_gridLayout.addWidget(self.Sellprice_Label, 3, 0, 1, 1)

        self.Sellprice_LineEdit = QtWidgets.QLineEdit()
        self.Sellprice_LineEdit.setFont(self.font)
        self.Sellprice_LineEdit.setFixedWidth(150)
        self.Sellprice_LineEdit.editingFinished.connect(lambda: self.Date_DateEdit.setFocus())
        self.input_gridLayout.addWidget(self.Sellprice_LineEdit, 3, 1, 1, 1)
        #-------------------------------------------------------------

        #Date
        self.Date_Label = QtWidgets.QLabel('Date :')
        self.Date_Label.setFont(self.font)
        self.Date_Label.setAlignment(QtCore.Qt.AlignRight)
        self.Date_Label.setFixedWidth(100)
        self.input_gridLayout.addWidget(self.Date_Label, 4, 0, 1, 1)

        self.Date_DateEdit = QtWidgets.QDateEdit()
        self.Date_DateEdit.setFont(self.font)
        self.Date_DateEdit.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.Date_DateEdit.setDisplayFormat('MM/yyyy')
        self.Date_DateEdit.setToolTip('mm/yyyy')
        self.Date_DateEdit.setDate(QtCore.QDate(int(date.today().strftime('%Y')),int(date.today().strftime('%m')),10))
        self.Date_DateEdit.editingFinished.connect(lambda: self.Quantity_LineEdit.setFocus())
        self.Date_DateEdit.setFixedWidth(150)
        self.input_gridLayout.addWidget(self.Date_DateEdit, 4, 1, 1, 1)
        #-------------------------------------------------------------

        #Quantity
        self.Quantity_Label = QtWidgets.QLabel('Quantity :')
        self.Quantity_Label.setFont(self.font)
        self.Quantity_Label.setAlignment(QtCore.Qt.AlignRight)
        self.Quantity_Label.setFixedWidth(100)
        self.input_gridLayout.addWidget(self.Quantity_Label, 5, 0, 1, 1)

        self.Quantity_LineEdit = QtWidgets.QLineEdit()
        self.Quantity_LineEdit.setFont(self.font)
        self.Quantity_LineEdit.setFixedWidth(150)
        self.input_gridLayout.addWidget(self.Quantity_LineEdit, 5, 1, 1, 1)
        #-------------------------------------------------------------

        #Enter
        self.Enter_Button = QtWidgets.QPushButton('Enter', clicked = lambda: self.clicked_enter())
        self.Enter_Button.setFont(self.font)
        self.Enter_Button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.input_gridLayout.addWidget(self.Enter_Button, 0,2,6,1)
        #-------------------------------------------------------------

        #Confirm
        self.Confirm_Button = QtWidgets.QPushButton('Confirm', clicked = lambda: self.clicked_confirm())
        self.Confirm_Button.setFont(self.font)
        self.main_gridLayout.addWidget(self.Confirm_Button, 1,1,1,1)
        #-------------------------------------------------------------

        #show_input_info
        self.show_input_info = QtWidgets.QTableWidget()
        self.main_gridLayout.addWidget(self.show_input_info,0,0,1,1)
        self.show_input_info.setMinimumWidth(600)
        self.setdatain_show_input_info()  
        self.show_input_info.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.show_input_info.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        #---------------------------------------------------------------

        #Delete
        self.Delete_Button = QtWidgets.QPushButton('Delete', clicked = lambda: self.clicked_delete())
        self.Delete_Button.setFont(self.font)
        self.main_gridLayout.addWidget(self.Delete_Button, 1,0,1,1)
        #---------------------------------------------------------

    def setdatain_show_input_info(self):
        self.show_input_info.setColumnCount(7)
        self.show_input_info.setRowCount(len(self.input_info['Name']))
        Header = []
        for n,key in enumerate(self.input_info.keys()):
            Header.append(key)
            for m, item in enumerate(self.input_info[key]):
                newitem = QtWidgets.QTableWidgetItem(item)
                self.show_input_info.setItem(m, n, newitem)
            self.show_input_info.setHorizontalHeaderLabels(Header)

    def clicked_enter(self):
        Name = self.Name_LineEdit.text()
        Supplier = self.Supplier_LineEdit.text()
        Cost = self.Cost_LineEdit.text()
        Sellprice = self.Sellprice_LineEdit.text()
        D = str(self.Date_DateEdit.date().toPyDate())
        Month = D.split('-')[1]
        Year = D.split('-')[0][2:]
        Quantity = self.Quantity_LineEdit.text()

        if (Name and Supplier != '') and (Cost.isnumeric() and Sellprice.isnumeric() and Quantity.isnumeric() == True):
            self.input_info['Name'].append(Name)
            self.input_info['Supplier'].append(Supplier)
            self.input_info['Cost'].append(Cost)
            self.input_info['Sell price'].append(Sellprice)
            self.input_info['Month'].append(Month)
            self.input_info['Year'].append(Year)
            self.input_info['Quantity'].append(Quantity)
            self.setdatain_show_input_info()
            self.Name_LineEdit.clear()
            self.Cost_LineEdit.clear()
            self.Sellprice_LineEdit.clear()
            self.Quantity_LineEdit.clear()

    def clicked_confirm(self):
        if self.input_info['Name']:
            name_list = []
            quantity_list = []
            for i in range(0,len(self.input_info['Name'])):
                Name = self.input_info['Name'][i]
                Supplier = self.input_info['Supplier'][i]
                Cost = int(self.input_info['Cost'][i])
                Sellprice = int(self.input_info['Sell price'][i])
                Month = self.input_info['Month'][i]
                Year = self.input_info['Year'][i]
                Quantity = int(self.input_info['Quantity'][i])
                quantity_list.append(Quantity)
                Code = get_Code_Number(Name, Supplier, Month, Year)
                name_list.append(Code)
                save_css_from_code(Code,Cost,Sellprice,Quantity) #save new data to datase
                create_barcode(Code,sellcode='jhgffgfrfg') #create barcode
            
            print_barcode_to_pdf(name_list, quantity_list) #move barcode to pdf file and merge pdf file to one file in bercode folder
            self.input_info = {'Name':[],'Supplier':[],'Cost':[],'Sell price':[],'Month':[],'Year':[],'Quantity':[]}
            self.setdatain_show_input_info()
                
                
    def clicked_delete(self):
        row = self.show_input_info.currentRow()
        if row != -1:

            for i in self.input_info.keys():
                self.input_info[i].pop(row)

            self.setdatain_show_input_info()
    
    def SupplierName_LineEdit_Finish(self):
        Supplier = self.Supplier_LineEdit.text()
        Name = self.Name_LineEdit.text()
        if Supplier and Name != '':
            Code = get_Code_Number(Name,Supplier,'01','22')[:-4]
            for n,i in enumerate(self.css_file['Code']):
                if Code == i:
                    Cost = self.css_file['Cost'][n]
                    Sellprice = self.css_file['Sellprice'][n]
                    self.Cost_LineEdit.setText(Cost)
                    self.Sellprice_LineEdit.setText(Sellprice)
                    self.Date_DateEdit.setFocus()
        else:
            self.Cost_LineEdit.setFocus()

    def Cost_LineEdit_Finish(self):
        Cost = self.Cost_LineEdit.text()
        if Cost[:-1].isnumeric() == True and Cost[-1] == '+':
            Sellprice = sell_price_cal(int(Cost[:-1]))
            self.Cost_LineEdit.setText(Cost[:-1])
            self.Sellprice_LineEdit.setText(str(Sellprice))
            self.Sellprice_LineEdit.setFocus()
        else:
            self.Sellprice_LineEdit.setFocus()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Restock_Window()
    window.show()
    sys.exit(app.exec_())
    
