from PyQt5 import QtGui, QtWidgets
import threading

from client import send

class FinalWindow(QtWidgets.QMainWindow):
    def __init__(self,total_sum,out_info,total_cost):
        super(FinalWindow, self).__init__()
        self.font = QtGui.QFont()
        self.font.setPointSize(16)
        self.total_sum = total_sum
        self.out_info = out_info
        self.total_cost = total_cost
        self.setupUI()
    
    def setupUI(self):
        self.resize(300,100)
        self.setMaximumSize(300,100)
        self.gridLayoutWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.gridLayoutWidget)
        self.main_gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)

        #All sum
        self.Allsum_Label = QtWidgets.QLabel('ราคารวม : ')
        self.Allsum_Label.setFont(self.font)
        self.main_gridLayout.addWidget(self.Allsum_Label, 0, 0, 1, 1)

        self.Allsum_LineEdit = QtWidgets.QLineEdit(str(self.total_sum))
        self.Allsum_LineEdit.setFont(self.font)
        self.Allsum_LineEdit.setEnabled(False)
        self.main_gridLayout.addWidget(self.Allsum_LineEdit, 0, 1, 1, 1)
        #----------------------------------------------------------------

        #Cash
        self.Cash_Label = QtWidgets.QLabel('เงิน : ')
        self.Cash_Label.setFont(self.font)
        self.main_gridLayout.addWidget(self.Cash_Label, 1, 0, 1, 1)

        self.Cash_LineEdit = QtWidgets.QLineEdit()
        self.Cash_LineEdit.setFont(self.font)
        self.Cash_LineEdit.textChanged.connect(self.change_calculate)
        self.main_gridLayout.addWidget(self.Cash_LineEdit, 1, 1, 1, 1)
        #----------------------------------------------------------------

        #Change
        self.Change_Label = QtWidgets.QLabel('เงินทอน : ')
        self.Change_Label.setFont(self.font)
        self.main_gridLayout.addWidget(self.Change_Label, 2, 0, 1, 1)

        self.Change_LineEdit = QtWidgets.QLineEdit()
        self.Change_LineEdit.setFont(self.font)
        self.main_gridLayout.addWidget(self.Change_LineEdit, 2, 1, 1, 1)
        self.Change_LineEdit.setEnabled(False)
        #---------------------------------------------

        #Finish
        self.Finish_Button = QtWidgets.QPushButton('เสร็จสิ้น')
        self.Finish_Button.setFont(self.font)
        self.Finish_Button.clicked.connect(self.clicked_finish)
        self.main_gridLayout.addWidget(self.Finish_Button, 3, 1, 1, 1)
        self.Finish_Button.setEnabled(False)
        #---------------------------------------------

    def change_calculate(self):
        Cash_input = self.Cash_LineEdit.text()
        if Cash_input.isnumeric() and int(Cash_input) >= self.total_sum:
            self.Change_LineEdit.setText(str(int(Cash_input)-self.total_sum))
            self.Finish_Button.setEnabled(True)
        elif Cash_input.isnumeric() == False or int(Cash_input) < self.total_sum:
            self.Change_LineEdit.setText('')
            self.Finish_Button.setEnabled(False)

    def clicked_finish(self):
        output = dict()
        #set output
        output['Code'] = self.out_info['Code']
        output['Quantity'] = self.out_info['Quantity']
        output['All'] = [str(self.total_sum), str(self.total_cost)]
        out_data = []
        client = threading.Thread(target=send, args=('dict',output,out_data))
        client.start()
        self.Finish_Button.setEnabled(False)
        self.Change_LineEdit.setText('')
        self.Cash_LineEdit.setText('')
        self.hide()
