from webbrowser import get
from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd
from main import get_nsd_from_code

class Stock_Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Stock_Window, self).__init__()
        self.setWindowTitle('Check Stock Window')
        self.font = QtGui.QFont()
        self.font.setPointSize(12)
        self.input_info = dict()
        self.column_filter_Label = ''
        self.column_num = -1
        self.setupUi()

    def setupinfo(self):
        self.input_info['Name'] = []
        self.input_info['Supplier'] = []
        self.input_info.update(pd.read_csv('Cost_Sellprice_Stock.csv', dtype=str).to_dict('list'))
        for n in self.input_info['Code']:
            nsd = get_nsd_from_code(n)
            self.input_info['Name'].append(nsd[0])
            self.input_info['Supplier'].append(nsd[1])
        self.filter_dict = self.input_info.copy()

    def setupUi(self):
        self.setupinfo()
        self.resize(675, 488)
        self.move(20,20)
        self.gridLayoutWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.gridLayoutWidget)
        self.main_gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)

        #Filter
        self.Filter_Label = QtWidgets.QLabel('Filter : ')
        self.Filter_Label.setFont(self.font)
        self.Filter_Label.setAlignment(QtCore.Qt.AlignRight)
        self.Filter_Label.setFixedWidth(120) 
        self.main_gridLayout.addWidget(self.Filter_Label,0,0,1,1)

        self.Filter_LineEdit = QtWidgets.QLineEdit()
        self.Filter_LineEdit.setFont(self.font)
        self.Filter_LineEdit.textChanged.connect(self.filter)
        self.main_gridLayout.addWidget(self.Filter_LineEdit,0,1,1,1)

        self.Deselect_Button = QtWidgets.QPushButton('Deselect')
        self.Deselect_Button.clicked.connect(self.deselction)
        self.Deselect_Button.setFont(self.font)
        self.Deselect_Button.setFixedWidth(100)
        self.main_gridLayout.addWidget(self.Deselect_Button,0,2,1,1)
        #---------------------------------------------------------------
        
        #show_input_info
        self.show_input_info = QtWidgets.QTableWidget()
        self.main_gridLayout.addWidget(self.show_input_info,1,0,1,3)
        self.show_input_info.setMinimumWidth(600)
        self.setdatain_show_input_info()  
        self.show_input_info.selectionModel().selectionChanged.connect(self.changeselection)
        self.show_input_info.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.show_input_info.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        #---------------------------------------------------------------

        #Edit
        self.Edit_Button = QtWidgets.QPushButton('Edit')
        self.Edit_Button.clicked.connect(self.EditWindow)
        self.Edit_Button.setFont(self.font)
        self.main_gridLayout.addWidget(self.Edit_Button,2,0,1,3)
        #---------------------------------------------------------------

        #Sort shortcut
        self.Sort_Shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+Shift+S"), self)
        self.Sort_Shortcut.activated.connect(self.sort_table)
        #----------------------------------------------------------------------

    def changeselection(self):
        if self.show_input_info.currentColumn() != -1: #-1 is normal value of deselection state of pyqt5
            self.column_num = self.show_input_info.currentColumn()
            if self.column_num >= 0:
                self.column_filter_Label = list(self.input_info.keys())[self.show_input_info.currentColumn()]
                self.Filter_Label.setText(f'{self.column_filter_Label} Filter : ')

    def sort_table(self):
        if self.column_num >= 0:
            self.show_input_info.sortItems(self.column_num, QtCore.Qt.AscendingOrder)
    
    def deselction(self):
        self.show_input_info.clearSelection()
        self.column_num = -2
        self.Filter_LineEdit.setText('')
        self.column_filter_Label = ''
        self.Filter_Label.setText(f'{self.column_filter_Label} Filter : ')

    def filter(self):
        filter_input = self.Filter_LineEdit.text()
        if self.column_num == 1: #if column supplier is selected turn user input to uppercase
            filter_input = filter_input.upper()

        if self.column_num >= 0:
            column_name = list(self.input_info.keys())[self.column_num]
            filter_list = []

            for n,v in enumerate(self.input_info[column_name]): #get list of index of value that match the input
                if filter_input in v:
                    filter_list.append(n)

            for k,v in self.input_info.items(): #filter dict to match the filter_list
                l = []
                for n,w in enumerate(v):
                    if n in filter_list:
                        l.append(w)
                self.filter_dict[k] = l

        elif self.column_num < 0: #if no column is selected return un filter table
            self.filter_dict = self.input_info.copy()

        self.setdatain_show_input_info()



    def setdatain_show_input_info(self):
        self.show_input_info.setColumnCount(6)
        self.show_input_info.setRowCount(len(self.filter_dict['Code']))
        Header = ['Name','Supplier','Code','Cost','Sell price','Stock']
        for n,key in enumerate(self.filter_dict.keys()):
            for m, item in enumerate(self.filter_dict[key]):
                newitem = QtWidgets.QTableWidgetItem(item)
                self.show_input_info.setItem(m, n, newitem)
            self.show_input_info.setHorizontalHeaderLabels(Header)

    def EditWindow(self):
        row_num = self.show_input_info.currentRow()
        global edit_list
        edit_list = [self.filter_dict[k][row_num] for k in self.filter_dict.keys()]
        self.sub_window = Edit_Window()
        self.sub_window.show()
        global mainwindow
        mainwindow = self

class Edit_Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Edit_Window, self).__init__()
        self.setWindowTitle('Edit Window')
        self.font = QtGui.QFont()
        self.font.setPointSize(12)
        self.setupUi()

    def setupUi(self):
        print(edit_list[2])
        self.resize(400, 200)
        self.setFixedSize(400,200)
        self.move(20,20)
        self.gridLayoutWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.gridLayoutWidget)
        self.main_gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)

        #Name 
        self.Name_Label = QtWidgets.QLabel('Name : ')
        self.Name_Label.setFont(self.font)
        self.main_gridLayout.addWidget(self.Name_Label,0,0,1,1)

        self.Name_LineEdit = QtWidgets.QLineEdit(edit_list[0])
        self.Name_LineEdit.setFont(self.font)
        self.Name_LineEdit.setEnabled(False)
        self.main_gridLayout.addWidget(self.Name_LineEdit,0,1,1,1)
        #---------------------------------------------------------------

        #Supplier
        self.Supplier_Label = QtWidgets.QLabel('Supplier : ')
        self.Supplier_Label.setFont(self.font)
        self.main_gridLayout.addWidget(self.Supplier_Label,1,0,1,1)

        self.Supplier_LineEdit = QtWidgets.QLineEdit(edit_list[1])
        self.Supplier_LineEdit.setFont(self.font)
        self.Supplier_LineEdit.setEnabled(False)
        self.main_gridLayout.addWidget(self.Supplier_LineEdit,1,1,1,1)
        #---------------------------------------------------------------

        #Cost
        self.Cost_Label = QtWidgets.QLabel('Cost : ')
        self.Cost_Label.setFont(self.font)
        self.main_gridLayout.addWidget(self.Cost_Label,2,0,1,1)

        self.Cost_LineEdit = QtWidgets.QLineEdit(edit_list[3])
        self.Cost_LineEdit.setFont(self.font)
        self.main_gridLayout.addWidget(self.Cost_LineEdit,2,1,1,1)
        #---------------------------------------------------------------

        #Sell price
        self.Sellprice_Label = QtWidgets.QLabel('Sell price : ')
        self.Sellprice_Label.setFont(self.font)
        self.main_gridLayout.addWidget(self.Sellprice_Label,3,0,1,1)

        self.Sellprice_LineEdit = QtWidgets.QLineEdit(edit_list[4])
        self.Sellprice_LineEdit.setFont(self.font)
        self.main_gridLayout.addWidget(self.Sellprice_LineEdit,3,1,1,1)
        #---------------------------------------------------------------

        #Stock
        self.Stock_Label = QtWidgets.QLabel('Stock : ')
        self.Stock_Label.setFont(self.font)
        self.main_gridLayout.addWidget(self.Stock_Label,4,0,1,1)

        self.Stock_LineEdit = QtWidgets.QLineEdit(edit_list[5])
        self.Stock_LineEdit.setFont(self.font)
        self.main_gridLayout.addWidget(self.Stock_LineEdit,4,1,1,1)
        #---------------------------------------------------------------

        #apply
        self.Apply_Button = QtWidgets.QPushButton('Apply')
        self.Apply_Button.setFont(self.font)
        self.Apply_Button.clicked.connect(self.clicked_apply)
        self.main_gridLayout.addWidget(self.Apply_Button,5,1,1,1)
        #---------------------------------------------------------------

    def clicked_apply(self):
        Cost = self.Cost_LineEdit.text()
        Sellprice = self.Sellprice_LineEdit.text()
        Stock = self.Stock_LineEdit.text()
        df = pd.read_csv('Cost_Sellprice_Stock.csv', dtype=str)

        if (Cost.isnumeric() and Sellprice.isnumeric() and Stock.isnumeric() == True):
            row = df.query(f'Code == "{edit_list[2]}" and Cost == "{edit_list[3]}" and Sellprice == "{edit_list[4]}" and Stock == "{edit_list[5]}"').index
            df.loc[row] = [edit_list[2],Cost,Sellprice,Stock]
            df.to_csv('Cost_Sellprice_Stock.csv', index=False,encoding='utf-8')
    

        mainwindow.setupUi()
        self.close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication([])
    window = Stock_Window()
    window.show()
    sys.exit(app.exec_())
