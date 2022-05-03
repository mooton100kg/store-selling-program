import sys
from PyQt5 import QtGui, QtWidgets
import pandas as pd

class AlertWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(AlertWindow, self).__init__()
        self.resize(675, 488)
        self.font = QtGui.QFont()
        self.font.setPointSize(24)
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle('Stock Alert')
        self.gridLayoutWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.gridLayoutWidget)
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)

        #alert list
        self.Alert_Table = QtWidgets.QTableWidget()
        self.clicked_checkstock()
        self.Alert_Table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.gridLayout.addWidget(self.Alert_Table,0,0,1,1)

        #check stock
        self.Checkstock_Button = QtWidgets.QPushButton('Check Stock')
        self.Checkstock_Button.setFont(self.font)
        self.Checkstock_Button.clicked.connect(self.clicked_checkstock)
        self.gridLayout.addWidget(self.Checkstock_Button,1,0,1,1) 


    def clicked_checkstock(self):
        self.css = pd.read_csv('database/Cost_Sellprice_Stock.csv',dtype=str)
        self.ra = pd.read_csv('database/Restock_Alert.csv', dtype=str)
        self.table_info = {'Code':[],'Quantity':[],'Minimum':[],'Archive':[]}

        for row_css,c in enumerate(list(self.css['Code'])):
            quantity = int(self.css['Stock'][row_css])
            row_ra = self.ra[self.ra['Code'] == c].index[0]
            min = int(self.ra['Minimum'][row_ra])
            alert = self.ra['Alert'][row_ra]

            if quantity < min and alert != '1':
                self.table_info['Code'].append(c)
                self.table_info['Quantity'].append(str(quantity))
                self.table_info['Minimum'].append(str(min))

                self.Archive_Button = QtWidgets.QPushButton('Archive')
                self.Archive_Button.clicked.connect(self.handleButtonClicked)
                self.table_info['Archive'].append(self.Archive_Button)
        self.setdatain_table()

    def setdatain_table(self):
        self.Alert_Table.setColumnCount(4)
        self.Alert_Table.setRowCount(len(self.table_info['Code']))
        Header = ['Code','Quantity','Minimum','Archive']
        for n,key in enumerate(Header):
            for m, item in enumerate(self.table_info[key]):
                if key != 'Archive':
                    newitem = QtWidgets.QTableWidgetItem(item)
                    self.Alert_Table.setItem(m, n, newitem)
                elif key == 'Archive':
                    self.Alert_Table.setCellWidget(m,n,item)
            self.Alert_Table.setHorizontalHeaderLabels(Header)

    def handleButtonClicked(self):
        button = QtWidgets.qApp.focusWidget()
        button.setEnabled(False)
        index = self.Alert_Table.indexAt(button.pos())
        if index.isValid():
            code = self.Alert_Table.item(index.row(),0).text()
            min = self.Alert_Table.item(index.row(),2).text()
            row_ra = self.ra[self.ra['Code'] == code].index[0]

            self.ra.loc[row_ra] = [code, min,'1'] 
            self.ra.to_csv('database/Restock_Alert.csv', index=False, encoding='utf-8')

            for c in range(self.Alert_Table.columnCount()-1):
                self.Alert_Table.item(index.row(),c).setBackground(QtGui.QColor(111,111,111))
            
