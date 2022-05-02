from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import pandas as pd
from datetime import date

from func import update_bill

class SupplierbillWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(SupplierbillWindow, self).__init__()
        self.font = QtGui.QFont()
        self.font.setPointSize(16)
        self.Supplier_number = pd.read_csv('Code number/Supplier number.csv', dtype=str)
        self.input_info = {'Supplier':[],'Bill number':[],'Bill date':[],'Total cost':[],'Month':[],'Year':[]}
        self.setupUi()

    def setupUi(self):
        self.resize(594, 522)
        self.gridLayoutWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.gridLayoutWidget)
        self.main_gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        
        #sub grideLayout
        self.input_gridLayout = QtWidgets.QGridLayout()
        self.main_gridLayout.addLayout(self.input_gridLayout, 0,1,1,1)


        #Supplier
        self.Supplier_Label = QtWidgets.QLabel('Supplier :')
        self.Supplier_Label.setFont(self.font)
        self.Supplier_Label.setAlignment(QtCore.Qt.AlignRight)
        self.Supplier_Label.setFixedWidth(125)
        self.input_gridLayout.addWidget(self.Supplier_Label, 0, 0, 1, 1)

        self.Supplier_LineEdit = QtWidgets.QLineEdit()
        self.Supplier_LineEdit.setFont(self.font)
        self.Supplier_LineEdit.setFixedWidth(150)
        self.Supplier_LineEdit.editingFinished.connect(lambda: self.Supplier_LineEdit.setFocus())
        self.Supplier_LineEdit.setCompleter(QtWidgets.QCompleter(self.Supplier_number['Supplier'].to_list()))
        self.input_gridLayout.addWidget(self.Supplier_LineEdit, 0, 1, 1, 1)
        #-------------------------------------------------------------

        #Billnumber
        self.Billnumber_Label = QtWidgets.QLabel('Billnumber :')
        self.Billnumber_Label.setFont(self.font)
        self.Billnumber_Label.setAlignment(QtCore.Qt.AlignRight)
        self.Billnumber_Label.setFixedWidth(125)
        self.input_gridLayout.addWidget(self.Billnumber_Label, 1, 0, 1, 1)

        self.Billnumber_LineEdit = QtWidgets.QLineEdit()
        self.Billnumber_LineEdit.setFont(self.font)
        self.Billnumber_LineEdit.setFixedWidth(150)
        self.input_gridLayout.addWidget(self.Billnumber_LineEdit, 1, 1, 1, 1)
        #-------------------------------------------------------------

        #Billdate
        self.Billdate_Label = QtWidgets.QLabel('Billdate :')
        self.Billdate_Label.setFont(self.font)
        self.Billdate_Label.setAlignment(QtCore.Qt.AlignRight)
        self.Billdate_Label.setFixedWidth(125)
        self.input_gridLayout.addWidget(self.Billdate_Label, 2, 0, 1, 1)

        self.Billdate_DateEdit = QtWidgets.QDateEdit()
        self.Billdate_DateEdit.setFont(self.font)
        self.Billdate_DateEdit.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.Billdate_DateEdit.setDisplayFormat('dd/MM/yyyy')
        self.Billdate_DateEdit.setToolTip('dd/mm/yyyy')
        self.Billdate_DateEdit.setDate(QtCore.QDate(int(date.today().strftime('%Y')),int(date.today().strftime('%m')),int(date.today().strftime('%d'))-1))
        self.Billdate_DateEdit.editingFinished.connect(lambda: self.Quantity_LineEdit.setFocus())
        self.Billdate_DateEdit.setFixedWidth(150)
        self.input_gridLayout.addWidget(self.Billdate_DateEdit, 2, 1, 1, 1)
        #-------------------------------------------------------------

        #Totalcost
        self.Totalcost_Label = QtWidgets.QLabel('Totalcost :')
        self.Totalcost_Label.setFont(self.font)
        self.Totalcost_Label.setAlignment(QtCore.Qt.AlignRight)
        self.Totalcost_Label.setFixedWidth(125)
        self.input_gridLayout.addWidget(self.Totalcost_Label, 3, 0, 1, 1)

        self.Totalcost_LineEdit = QtWidgets.QLineEdit()
        self.Totalcost_LineEdit.setFont(self.font)
        self.Totalcost_LineEdit.setFixedWidth(150)
        self.input_gridLayout.addWidget(self.Totalcost_LineEdit, 3, 1, 1, 1)
        #-------------------------------------------------------------

        #Enter
        self.Enter_Button = QtWidgets.QPushButton('Enter', clicked = lambda: self.clicked_enter())
        self.Enter_Button.setFont(self.font)
        self.Enter_Button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.input_gridLayout.addWidget(self.Enter_Button, 0,2,4,1)
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
        self.show_input_info.setColumnCount(6)
        self.show_input_info.setRowCount(len(self.input_info['Supplier']))
        Header = []
        for n,key in enumerate(self.input_info.keys()):
            Header.append(key)
            for m, item in enumerate(self.input_info[key]):
                newitem = QtWidgets.QTableWidgetItem(item)
                self.show_input_info.setItem(m, n, newitem)
            self.show_input_info.setHorizontalHeaderLabels(Header)

    def clicked_enter(self):
        Supplier = self.Supplier_LineEdit.text()
        Billnumber = self.Billnumber_LineEdit.text()
        D = str(self.Billdate_DateEdit.date().toPyDate())
        Totalcost = self.Totalcost_LineEdit.text()
        Day = D.split('-')[2]
        Month = D.split('-')[1]
        Year = D.split('-')[0]
        D = f'{Day}-{Month}-{Year}'

        if (Billnumber and Supplier != '') and Totalcost.isnumeric() == True:
            self.input_info['Supplier'].append(Supplier)
            self.input_info['Bill number'].append(Billnumber)
            self.input_info['Bill date'].append(D)
            self.input_info['Total cost'].append(Totalcost)
            self.input_info['Month'].append(Month)
            self.input_info['Year'].append(Year)
            self.setdatain_show_input_info()
            self.Supplier_LineEdit.clear()
            self.Billnumber_LineEdit.clear()
            self.Totalcost_LineEdit.clear()

    def clicked_confirm(self):
        if self.input_info['Supplier']:
            for i in range(0,len(self.input_info['Supplier'])):
                Supplier = self.input_info['Supplier'][i]
                Billnumber = self.input_info['Bill number'][i]
                Billdate = self.input_info['Bill date'][i]
                Totalcost = self.input_info['Total cost'][i]
                Month = self.input_info['Month'][i]
                Year = self.input_info['Year'][i]
            
                update_bill(Supplier, Billnumber, Billdate, Totalcost, Month, Year) #save data to csv
            self.input_info = {'Supplier':[],'Bill number':[],'Bill date':[],'Total cost':[],'Month':[],'Year':[]}
            self.setdatain_show_input_info()
                
                
    def clicked_delete(self):
        row = self.show_input_info.currentRow()
        if row != -1:

            for i in self.input_info.keys():
                self.input_info[i].pop(row)

            self.setdatain_show_input_info()
    



