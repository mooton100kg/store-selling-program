from PyQt5 import QtCore, QtGui, QtWidgets
import threading,time

from client import send,start
from sup_window import FinalWindow

class Client_Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Client_Window, self).__init__()
        self.input_info = {'Code':[], 'Name':[], 'Sell price/unit':[], 'Quantity':[],'Stock':[], 'Sell price':[], 'Cost/unit':[], 'Cost':[]}
        self.font = QtGui.QFont()
        self.font.setPointSize(16)
        self.Allsum = 0
        self.setupUi()

    def setupUi(self):
        self.resize(675, 488)
        self.move(20,20)
        self.gridLayoutWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.gridLayoutWidget)
        self.main_gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)

        #sub gridLayout
        self.input_gridLayout = QtWidgets.QGridLayout()
        self.main_gridLayout.addLayout(self.input_gridLayout, 0, 3, 1, 1)

        #show_input_info
        self.show_input_info = QtWidgets.QTableWidget()
        self.main_gridLayout.addWidget(self.show_input_info, 0, 0, 1, 3)
        self.show_input_info.setMinimumWidth(800)
        self.setdatain_show_input_info()  
        self.show_input_info.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.show_input_info.setSelectionBehavior(1)
        self.show_input_info.selectionModel().selectionChanged.connect(self.changeselection)
        self.show_input_info.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.show_input_info.setEnabled(False)
        #-----------------------------------------------------------------------------------

        #all sum
        self.Allsum_Label = QtWidgets.QLabel('All sum :')
        self.Allsum_Label.setFont(self.font)
        self.main_gridLayout.addWidget(self.Allsum_Label, 1, 0, 1, 1)


        self.Allsum_LineEdit = QtWidgets.QLineEdit(str(self.Allsum))
        self.Allsum_LineEdit.setFont(self.font)
        self.main_gridLayout.addWidget(self.Allsum_LineEdit, 1, 1, 1, 1)
        self.Allsum_LineEdit.setEnabled(False)
        #----------------------------------------------------------------

        #Delete
        self.Delete_Button = QtWidgets.QPushButton('Delete')
        self.Delete_Button.setFont(self.font)
        self.Delete_Button.setFixedWidth(100)
        self.Delete_Button.clicked.connect(self.clicked_delete)
        self.main_gridLayout.addWidget(self.Delete_Button, 1, 2, 1, 1)
        self.Delete_Button.setEnabled(False)
        #----------------------------------------------------

        #Confirm
        self.Confirm_Button = QtWidgets.QPushButton('Confirm')
        self.Confirm_Button.setFont(self.font)
        self.Confirm_Button.setFixedHeight(50)
        self.Confirm_Button.clicked.connect(self.clicked_confirm)
        self.main_gridLayout.addWidget(self.Confirm_Button, 2, 0, 1, 3)
        self.Confirm_Button.setEnabled(False)
        #----------------------------------------------------------------

        #IP
        self.IP_LineEdit = QtWidgets.QLineEdit('192.168.1.25')
        self.IP_LineEdit.setFont(self.font)
        self.IP_LineEdit.setMinimumWidth(150)
        self.input_gridLayout.addWidget(self.IP_LineEdit, 0, 0, 1, 1)

        self.IP_Button = QtWidgets.QPushButton('Login')
        self.IP_Button.setFont(self.font)
        self.IP_Button.clicked.connect(self.clicked_login)
        self.input_gridLayout.addWidget(self.IP_Button, 0, 1, 1, 1)

        self.IPlogout_Button = QtWidgets.QPushButton('Logout')
        self.IPlogout_Button.setFont(self.font)
        self.IPlogout_Button.clicked.connect(self.clicked_logout)
        self.input_gridLayout.addWidget(self.IPlogout_Button, 0, 1, 1, 1)
        self.IPlogout_Button.hide()
        #----------------------------------------------------------------

        #Code
        self.Code_Label = QtWidgets.QLabel('Code : ')
        self.Code_Label.setFont(self.font)
        self.input_gridLayout.addWidget(self.Code_Label, 1, 0, 1, 1)

        self.Code_LineEdit = QtWidgets.QLineEdit()
        self.Code_LineEdit.setFont(self.font)
        self.Code_LineEdit.setFocus()
        self.Code_LineEdit.editingFinished.connect(lambda: self.enter_code())
        self.input_gridLayout.addWidget(self.Code_LineEdit, 1, 1, 1, 1)
        self.Code_LineEdit.setEnabled(False)
        #----------------------------------------------------------------

        #Quantity
        self.Quantity_Label = QtWidgets.QLabel('Quantity : ')
        self.Quantity_Label.setFont(self.font)
        self.input_gridLayout.addWidget(self.Quantity_Label, 2, 0, 1, 1)

        self.Quantity_LineEdit = QtWidgets.QSpinBox()
        self.Quantity_LineEdit.setFont(self.font)
        self.Quantity_LineEdit.setMinimum(1)
        self.Quantity_LineEdit.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.Quantity_LineEdit.setEnabled(False)
        self.input_gridLayout.addWidget(self.Quantity_LineEdit, 2, 1, 1, 1)
        #----------------------------------------------------------------

        #Enter
        self.Enter_Button = QtWidgets.QPushButton('Enter')
        self.Enter_Button.clicked.connect(self.clicked_enter)
        self.Enter_Button.setFont(self.font)
        self.input_gridLayout.addWidget(self.Enter_Button, 3, 0, 1, 2)
        self.Enter_Button.setEnabled(False)
        #----------------------------------------------------------------

    def clicked_logout(self):
        client = threading.Thread(target=send, args=('str ','!DISCONNECT!' ,[]))
        client.start()
        self.close()

    def clicked_login(self):
        IP = self.IP_LineEdit.text()
        self.IP_Button.hide()
        self.IPlogout_Button.show()
        if IP:
            start(IP)
            self.IP_LineEdit.setEnabled(False)
            self.IP_Button.setEnabled(False)
            self.show_input_info.setEnabled(True)
            self.Allsum_LineEdit.setEnabled(True)
            self.Code_LineEdit.setEnabled(True)
            self.Confirm_Button.setEnabled(True)

    def clicked_confirm(self):
        self.sub_window = FinalWindow(int(self.Allsum_LineEdit.text()),self.input_info,sum(int(x) for x in self.input_info['Cost']))
        self.sub_window.show()

        #reset data
        self.Code_LineEdit.setText('')
        self.Quantity_LineEdit.setValue(1)
        self.Allsum_LineEdit.setText('')
        self.Code_LineEdit.setEnabled(True)
        self.Quantity_LineEdit.setEnabled(False)
        self.Enter_Button.setEnabled(False)
        self.Delete_Button.setEnabled(False)
        self.input_info = {'Code':[], 'Name':[], 'Sell price/unit':[], 'Quantity':[],'Stock':[], 'Sell price':[], 'Cost/unit':[], 'Cost':[]}
        self.setdatain_show_input_info()

    def clicked_delete(self):
        for i in list(self.input_info.keys()):
            self.input_info[i].pop(self.row_num)
        self.setdatain_show_input_info()

        self.Quantity_LineEdit.setValue(1)
        self.Code_LineEdit.setText('')
        self.Code_LineEdit.setEnabled(True)
        self.Quantity_LineEdit.setEnabled(False)
        self.Enter_Button.setEnabled(False)

        self.SetTotal()

    def SetTotal(self):
        self.Allsum = sum(int(x) for x in self.input_info['Sell price'])
        self.Allsum_LineEdit.setText(str(self.Allsum))


    def clicked_enter(self):
        new_quantity = self.Quantity_LineEdit.value()
        sellpriceperunit = int(self.input_info['Sell price/unit'][self.row_num])
        costperunit = int(self.input_info['Cost/unit'][self.row_num])
        self.input_info['Quantity'][self.row_num] = str(new_quantity)
        sellprice = sellpriceperunit * new_quantity
        cost = costperunit * new_quantity
        self.input_info['Sell price'][self.row_num] = str(sellprice)
        self.input_info['Cost'][self.row_num] = str(cost)
        self.setdatain_show_input_info()

        self.Quantity_LineEdit.setValue(1)
        self.Code_LineEdit.setText('')
        self.Code_LineEdit.setEnabled(True)
        self.Quantity_LineEdit.setEnabled(False)
        self.Enter_Button.setEnabled(False)

        self.SetTotal()


    def changeselection(self):
        self.row_num = self.show_input_info.currentRow()
        self.Code_LineEdit.setText(self.input_info['Code'][self.row_num])
        self.Quantity_LineEdit.setValue(int(self.input_info['Quantity'][self.row_num]))
        self.Quantity_LineEdit.setMaximum(int(self.input_info['Stock'][self.row_num]))
        self.Code_LineEdit.setEnabled(False)
        self.Quantity_LineEdit.setEnabled(True)
        self.Quantity_LineEdit.setFocus()
        self.Enter_Button.setEnabled(True)
        self.Delete_Button.setEnabled(True)
        self.show_input_info.clearSelection()

    def enter_code(self):
        code_input = self.Code_LineEdit.text()

        if code_input.isnumeric() == True and len(code_input)==12:
            if code_input not in self.input_info['Code']:
                self.Quantity_LineEdit.setValue(1)
                out_data = []
                client = threading.Thread(target=send, args=('str ',code_input,out_data))
                client.start()

                while client.is_alive():
                    #wait for server to give output
                    time.sleep(0.1)
                
                if len(out_data[0]) != 1:  
                    if int(out_data[0]['Stock']) > 0:
                        self.input_info['Name'].append(out_data[0]['Name'])
                        self.input_info['Cost/unit'].append(out_data[0]['Cost'])
                        self.input_info['Sell price/unit'].append(out_data[0]['Sellprice'])
                        self.input_info['Quantity'].append('1')
                        self.input_info['Code'].append(code_input)
                        self.input_info['Sell price'].append(out_data[0]['Sellprice'])
                        self.input_info['Cost'].append(out_data[0]['Cost'])
                        self.input_info['Stock'].append(out_data[0]['Stock'])
                        self.setdatain_show_input_info()

            elif code_input in self.input_info['Code']:
                #scan already exit code will auto add 1 quantity to code in table
                row_num = self.input_info['Code'].index(code_input)
                quantity = str(int(self.input_info['Quantity'][row_num])+1)
                if int(quantity) > int(self.input_info['Stock'][row_num]):
                    self.input_info['Quantity'][row_num] = self.input_info['Stock'][row_num]
                elif int(quantity) <= int(self.input_info['Stock'][row_num]):
                    self.input_info['Quantity'][row_num] = quantity
                #change sell price
                sellprice = int(self.input_info['Quantity'][row_num]) * int(self.input_info['Sell price/unit'][row_num])
                cost = int(self.input_info['Quantity'][row_num]) * int(self.input_info['Cost/unit'][row_num])
                self.input_info['Sell price'][row_num] = str(sellprice)
                self.input_info['Cost'][row_num] = str(cost)
                self.setdatain_show_input_info()

            self.SetTotal()
            #set zero
            self.Quantity_LineEdit.setValue(1)
            self.Code_LineEdit.setText('')


    def setdatain_show_input_info(self):
        self.show_input_info.setColumnCount(6)
        self.show_input_info.setRowCount(len(self.input_info['Name']))
        Header = ['Code', 'Name', 'Sell price/unit', 'Quantity','Stock', 'Sell price']
        for n,key in enumerate(Header):
            for m, item in enumerate(self.input_info[key]):
                newitem = QtWidgets.QTableWidgetItem(item)
                self.show_input_info.setItem(m, n, newitem)
            self.show_input_info.setHorizontalHeaderLabels(Header)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication([])
    window = Client_Window()
    window.show()
    sys.exit(app.exec_())
