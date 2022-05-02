import sys
from PyQt5 import QtCore, QtGui, QtWidgets
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
        self.Alert_Table.setColumnCount(4)
        self.Alert_Table.setHorizontalHeaderLabels(['Code','Quantity','Check'])
        self.gridLayout.addWidget(self.Alert_Table,0,0,1,1)

        #check stock
        self.Checkstock_Button = QtWidgets.QPushButton('Check Stock')
        self.Checkstock_Button.setFont(self.font)
        self.Checkstock_Button.clicked.connect(self.clicked_checkstock)
        self.gridLayout.addWidget(self.Checkstock_Button,1,0,1,1) 

    def clicked_checkstock(self):
        css = pd.read_csv('database/Cost_Sellprice_Stock.csv',dtype=str)
        ra = pd.read_csv('database/Restock_Alert.csv', dtype=str)
        for r,c in enumerate(list(css['Code'])):
            print(r,c)

    def change(self,code,quantity):
        self.Alert_Table.setRowCount(self.Alert_Table.rowCount()+1)

        c = QtWidgets.QTableWidgetItem(code)
        self.Alert_Table.setItem(self.Alert_Table.rowCount()-1,0,c)

        q = QtWidgets.QTableWidgetItem(quantity)
        self.Alert_Table.setItem(self.Alert_Table.rowCount()-1,1,q)

        self.Archive_Button = QtWidgets.QPushButton('Archive')
        self.Alert_Table.setCellWidget(self.Alert_Table.rowCount()-1,2,self.Archive_Button)


app = QtWidgets.QApplication([])
window = AlertWindow()
window.show()
sys.exit(app.exec_())
