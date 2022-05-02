from PyQt5 import QtGui, QtWidgets

from database_sup_window import CodenumberViewWindow,StockWindow,SupplierbillViewWindow

class DatabaseWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(DatabaseWindow, self).__init__()
        self.setWindowTitle('Stock list Window')
        self.font = QtGui.QFont()
        self.font.setPointSize(24)
        self.setupUi()

    def openWindow(self, NameOpenWindow):
        self.sub_window = NameOpenWindow()
        self.sub_window.show()

    def setupUi(self):
        self.resize(675, 488)
        self.move(20,20)
        self.gridLayoutWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.gridLayoutWidget)
        self.main_gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)

        #Stock
        self.Stock_Button = QtWidgets.QPushButton('Check stock', clicked = lambda : self.openWindow(StockWindow))
        self.Stock_Button.setFont(self.font)
        self.Stock_Button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.main_gridLayout.addWidget(self.Stock_Button, 0, 0, 1, 1)
        #----------------------------------------------------------------

        #Supplier bill
        self.Bill_Button = QtWidgets.QPushButton('Supplier Bill', clicked = lambda : self.openWindow(SupplierbillViewWindow))
        self.Bill_Button.setFont(self.font)
        self.Bill_Button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.main_gridLayout.addWidget(self.Bill_Button, 1, 0, 1, 1)
        #----------------------------------------------------------------

        #Code number
        self.Code_Button = QtWidgets.QPushButton('Code number', clicked = lambda : self.openWindow(CodenumberViewWindow))
        self.Code_Button.setFont(self.font)
        self.Code_Button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.main_gridLayout.addWidget(self.Code_Button, 2, 0, 1, 1)
        #----------------------------------------------------------------


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication([])
    window = DatabaseWindow()
    window.show()
    sys.exit(app.exec_())
