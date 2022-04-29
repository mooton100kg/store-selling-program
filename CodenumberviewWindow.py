from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd

class Codenumberview_Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Codenumberview_Window, self).__init__()
        self.setWindowTitle('Check Stock Window')
        self.font = QtGui.QFont()
        self.font.setPointSize(12)
        self.column_filter_Label = ''
        self.column_num = -1
        self.setupUi()
        global file_name
        file_name = 'Code number/Part number.csv'

    def setupUi(self):
        self.Part_number = pd.read_csv('Code number/Part number.csv', dtype=str).to_dict('list')
        self.Supplier_number = pd.read_csv('Code number/Supplier number.csv', dtype=str).to_dict('list')
        self.input_info = self.Part_number
        self.filter_dict = self.input_info.copy()
        self.resize(675, 488)
        self.move(20,20)
        self.gridLayoutWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.gridLayoutWidget)
        self.main_gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)

        #sub grideLayout
        self.select_gridLayout = QtWidgets.QGridLayout()
        self.main_gridLayout.addLayout(self.select_gridLayout, 0,0,1,3)

        #Filter
        self.Filter_Label = QtWidgets.QLabel('Filter : ')
        self.Filter_Label.setFont(self.font)
        self.Filter_Label.setAlignment(QtCore.Qt.AlignRight)
        self.Filter_Label.setFixedWidth(120) 
        self.main_gridLayout.addWidget(self.Filter_Label,1,0,1,1)

        self.Filter_LineEdit = QtWidgets.QLineEdit()
        self.Filter_LineEdit.setFont(self.font)
        self.Filter_LineEdit.textChanged.connect(self.filter)
        self.main_gridLayout.addWidget(self.Filter_LineEdit,1,1,1,1)

        self.Deselect_Button = QtWidgets.QPushButton('Deselect')
        self.Deselect_Button.clicked.connect(self.deselction)
        self.Deselect_Button.setFont(self.font)
        self.Deselect_Button.setFixedWidth(100)
        self.main_gridLayout.addWidget(self.Deselect_Button,1,2,1,1)
        #---------------------------------------------------------------
        
        #show_input_info
        self.show_input_info = QtWidgets.QTableWidget()
        self.main_gridLayout.addWidget(self.show_input_info,2,0,1,3)
        self.show_input_info.setMinimumWidth(600)
        self.setdatain_show_input_info()  
        self.show_input_info.selectionModel().selectionChanged.connect(self.changeselection)
        self.show_input_info.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.show_input_info.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        #---------------------------------------------------------------

        #part suppier select
        self.Part_Button = QtWidgets.QPushButton('Part number')
        self.Part_Button.clicked.connect(self.settypePart)
        self.Part_Button.setFont(self.font)
        self.Part_Button.setFixedHeight(30)
        self.Part_Button.setEnabled(False)
        self.select_gridLayout.addWidget(self.Part_Button,0,0,1,1)

        self.Supplier_Button = QtWidgets.QPushButton('Supplier number')
        self.Supplier_Button.clicked.connect(self.settypeSupplier)
        self.Supplier_Button.setFont(self.font)
        self.Supplier_Button.setFixedHeight(30)
        self.select_gridLayout.addWidget(self.Supplier_Button,0,1,1,1)
        #---------------------------------------------------------------

        #Edit
        self.Edit_Button = QtWidgets.QPushButton('Edit')
        self.Edit_Button.clicked.connect(self.EditWindow)
        self.Edit_Button.setFont(self.font)
        self.main_gridLayout.addWidget(self.Edit_Button,3,0,1,3)
        #---------------------------------------------------------------

        #Sort shortcut
        self.Sort_Shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+Shift+S"), self)
        self.Sort_Shortcut.activated.connect(self.sort_table)
        #----------------------------------------------------------------------

    def settypePart(self):
        self.input_info = self.Part_number
        self.Part_Button.setEnabled(False)
        self.Supplier_Button.setEnabled(True)
        self.filter_dict = self.input_info.copy()
        self.setdatain_show_input_info()
        global file_name
        file_name = 'Code number/Part number.csv'

    def settypeSupplier(self):
        self.input_info = self.Supplier_number
        self.Part_Button.setEnabled(True)
        self.Supplier_Button.setEnabled(False)
        self.filter_dict = self.input_info.copy()
        self.setdatain_show_input_info()
        global file_name
        file_name = 'Code number/Supplier number.csv'

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
        if self.column_num == 1 and self.Supplier_Button.isEnabled() == False: #if column supplier is selected turn user input to uppercase
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
        self.show_input_info.setColumnCount(2)
        self.show_input_info.setRowCount(len(self.filter_dict[list(self.filter_dict)[0]]))
        Header = []
        for n,key in enumerate(self.filter_dict.keys()):
            Header.append(key)
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

        #Number code 
        self.Number_Label = QtWidgets.QLabel('Number code : ')
        self.Number_Label.setFont(self.font)
        self.main_gridLayout.addWidget(self.Number_Label,0,0,1,1)

        self.Number_LineEdit = QtWidgets.QLineEdit(edit_list[0])
        self.Number_LineEdit.setFont(self.font)
        self.Number_LineEdit.setEnabled(False)
        self.main_gridLayout.addWidget(self.Number_LineEdit,0,1,1,1)
        #---------------------------------------------------------------

        #Name
        self.Name_Label = QtWidgets.QLabel('Name : ')
        self.Name_Label.setFont(self.font)
        self.main_gridLayout.addWidget(self.Name_Label,1,0,1,1)

        self.Name_LineEdit = QtWidgets.QLineEdit(edit_list[1])
        self.Name_LineEdit.setFont(self.font)
        self.main_gridLayout.addWidget(self.Name_LineEdit,1,1,1,1)
        #---------------------------------------------------------------

        #apply
        self.Apply_Button = QtWidgets.QPushButton('Apply')
        self.Apply_Button.setFont(self.font)
        self.Apply_Button.clicked.connect(self.clicked_apply)
        self.main_gridLayout.addWidget(self.Apply_Button,2,1,1,1)
        #---------------------------------------------------------------

    def clicked_apply(self):
        Name = self.Name_LineEdit.text()
        df = pd.read_csv(file_name, dtype=str)

        if Name != '':
            key = [k for k in df.keys()]
            row = df.query(f'`{key[0]}` == "{edit_list[0]}" and `{key[1]}` == "{edit_list[1]}"').index
            df.loc[row] = [edit_list[0],Name]
            df.to_csv(file_name, index=False,encoding='utf-8')

        mainwindow.setupUi()
        self.close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication([])
    window = Codenumberview_Window()
    window.show()
    sys.exit(app.exec_())
