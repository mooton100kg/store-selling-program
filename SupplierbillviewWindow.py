from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd


class Supplierbillview_Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Supplierbillview_Window, self).__init__()
        self.setWindowTitle('Check Stock Window')
        self.font = QtGui.QFont()
        self.font.setPointSize(12)
        self.column_filter_Label = ''
        self.column_num = -1
        self.setupUi()

    def setupUi(self):
        self.input_info = pd.read_csv('Supplier_Bill.csv', dtype=str).to_dict('list')
        self.filter_dict = self.input_info.copy()
        self.resize(675, 488)
        self.move(20,20)
        self.gridLayoutWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.gridLayoutWidget)
        self.main_gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)

        #Filter
        self.Filter_Label = QtWidgets.QLabel('Filter : ')
        self.Filter_Label.setFont(self.font)
        self.Filter_Label.setAlignment(QtCore.Qt.AlignRight)
        self.Filter_Label.setFixedWidth(130) 
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
        if self.column_num == 0: #if column supplier is selected turn user input to uppercase
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
        self.show_input_info.setRowCount(len(self.filter_dict['Supplier']))
        Header = ['Supplier','Bill num','Bill date','Total cost','Month','Year']
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
        self.resize(400, 200)
        self.setFixedSize(400,200)
        self.move(20,20)
        self.gridLayoutWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.gridLayoutWidget)
        self.main_gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)

        #Supplier 
        self.Supplier_Label = QtWidgets.QLabel('Supplier : ')
        self.Supplier_Label.setFont(self.font)
        self.main_gridLayout.addWidget(self.Supplier_Label,0,0,1,1)

        self.Supplier_LineEdit = QtWidgets.QLineEdit(edit_list[0])
        self.Supplier_LineEdit.setFont(self.font)
        self.main_gridLayout.addWidget(self.Supplier_LineEdit,0,1,1,1)
        #---------------------------------------------------------------

        #Bill num
        self.Billnum_Label = QtWidgets.QLabel('Bill number : ')
        self.Billnum_Label.setFont(self.font)
        self.main_gridLayout.addWidget(self.Billnum_Label,1,0,1,1)

        self.Billnum_LineEdit = QtWidgets.QLineEdit(edit_list[1])
        self.Billnum_LineEdit.setFont(self.font)
        self.main_gridLayout.addWidget(self.Billnum_LineEdit,1,1,1,1)
        #---------------------------------------------------------------

        #Bill date
        self.Date_Label = QtWidgets.QLabel('Date : ')
        self.Date_Label.setFont(self.font)
        self.main_gridLayout.addWidget(self.Date_Label,2,0,1,1)

        self.Date_DateEdit = QtWidgets.QDateEdit()
        self.Date_DateEdit.setFont(self.font)
        self.Date_DateEdit.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.Date_DateEdit.setDisplayFormat('dd/MM/yyyy')
        self.Date_DateEdit.setToolTip('mm/yyyy')
        self.Date_DateEdit.setDate(QtCore.QDate(int(edit_list[5]),int(edit_list[4]),int(edit_list[2].split('-')[0])))
        self.main_gridLayout.addWidget(self.Date_DateEdit, 2, 1, 1, 1)
        #-------------------------------------------------------------

        #Total cost
        self.Totalcost_Label = QtWidgets.QLabel('Total cost : ')
        self.Totalcost_Label.setFont(self.font)
        self.main_gridLayout.addWidget(self.Totalcost_Label,3,0,1,1)

        self.Totalcost_LineEdit = QtWidgets.QLineEdit(edit_list[3])
        self.Totalcost_LineEdit.setFont(self.font)
        self.main_gridLayout.addWidget(self.Totalcost_LineEdit,3,1,1,1)
        #---------------------------------------------------------------

        #apply
        self.Apply_Button = QtWidgets.QPushButton('Apply')
        self.Apply_Button.setFont(self.font)
        self.Apply_Button.clicked.connect(self.clicked_apply)
        self.main_gridLayout.addWidget(self.Apply_Button,4,1,1,1)
        #---------------------------------------------------------------

    def clicked_apply(self):
        Supplier = self.Supplier_LineEdit.text()
        Billnum = self.Billnum_LineEdit.text()
        D = str(self.Date_DateEdit.date().toPyDate())
        Day = D.split('-')[2]
        Month = D.split('-')[1]
        Year = D.split('-')[0]
        D = f'{Day}-{Month}-{Year}'
        Totalcost = self.Totalcost_LineEdit.text()
        df = pd.read_csv('Supplier_Bill.csv', dtype=str)

        if (Supplier and Billnum != '') and Totalcost.isnumeric() == True:
            row = df.query(f'Supplier == "{edit_list[0]}" and `Bill num` == "{edit_list[1]}" and `Bill date` == "{edit_list[2]}" and `Total cost` == "{edit_list[3]}" and Month == "{edit_list[4]}" and Year == "{edit_list[5]}"').index
            df.loc[row] = [Supplier,Billnum,D,Totalcost,Month,Year]
            df.to_csv('Supplier_Bill.csv', index=False,encoding='utf-8')
    

        mainwindow.setupUi()
        self.close()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication([])
    window = Supplierbillview_Window()
    window.show()
    sys.exit(app.exec_())
