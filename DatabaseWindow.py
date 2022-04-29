from PyQt5 import QtCore, QtGui, QtWidgets
from StockWindow import Stock_Window
from SupplierbillviewWindow import Supplierbillview_Window
from CodenumberviewWindow import Codenumberview_Window

class Database_Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Database_Window, self).__init__()
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
        self.Stock_Button = QtWidgets.QPushButton('Check stock', clicked = lambda : self.openWindow(Stock_Window))
        self.Stock_Button.setFont(self.font)
        self.Stock_Button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.main_gridLayout.addWidget(self.Stock_Button, 0, 0, 1, 1)
        #----------------------------------------------------------------

        #Supplier bill
        self.Bill_Button = QtWidgets.QPushButton('Supplier Bill', clicked = lambda : self.openWindow(Supplierbillview_Window))
        self.Bill_Button.setFont(self.font)
        self.Bill_Button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.main_gridLayout.addWidget(self.Bill_Button, 1, 0, 1, 1)
        #----------------------------------------------------------------

        #Code number
        self.Code_Button = QtWidgets.QPushButton('Code number', clicked = lambda : self.openWindow(Codenumberview_Window))
        self.Code_Button.setFont(self.font)
        self.Code_Button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.main_gridLayout.addWidget(self.Code_Button, 2, 0, 1, 1)
        #----------------------------------------------------------------


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication([])
    window = Database_Window()
    window.show()
    sys.exit(app.exec_())
