from threading import main_thread
from PyQt5 import QtCore, QtGui, QtWidgets


class Alert_Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Alert_Window, self).__init__()
        self.resize(675, 488)
        self.font = QtGui.QFont()
        self.font.setPointSize(24)
        self.setupUi()
        global main_window
        main_window = self


    def setupUi(self):
        self.setWindowTitle('Stock Alert')
        self.gridLayoutWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.gridLayoutWidget)
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)

        #alert list
        self.Alert_Table = QtWidgets.QTableWidget()
        self.Alert_Table.setColumnCount(4)
        self.Alert_Table.setRowCount(3)
        self.gridLayout.addWidget(self.Alert_Table,0,0,1,1)

        self.bb = QtWidgets.QPushButton('bb')
        self.bb.clicked.connect(self.clicked)
        self.gridLayout.addWidget(self.bb, 1,0,1,1)

    def clicked(self):
        print(type(self.Alert_Table.rowCount()))

    def change(self,code,quantity):
        c = QtWidgets.QTableWidgetItem(code)
        self.Alert_Table.setItem(self.Alert_Table.rowCount(),0,c)

        q = QtWidgets.QTableWidgetItem(quantity)
        self.Alert_Table.setItem(self.Alert_Table.rowCount(),1,q)

        self.btn_sell = QtWidgets.QPushButton('Edit')
        #self.btn_sell.clicked.connect(self.handleButtonClicked)
        self.table.setCellWidget(self.Alert_Table.rowCount(),2,self.btn_sell)

def stock_alert(code:str,quantity:int):
    main_window.change(code,quantity)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication([])
    window = Alert_Window()
    window.show()
    sys.exit(app.exec_())
