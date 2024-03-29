from PyQt5 import QtCore, QtGui, QtWidgets

from main_sup_window import DatabaseWindow,RestockWindow,ServerWindow,SupplierbillWindow
from main_sup_window.alert_window import AlertWindow

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(675, 488)
        self.font = QtGui.QFont()
        self.font.setPointSize(24)
        self.setWindowTitle('Main Window')
        self.setupUi()

    def openWindow(self, NameOpenWindow):
        self.sub_window = NameOpenWindow()
        self.sub_window.show()

    def setupUi(self):
        self.gridLayoutWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.gridLayoutWidget)
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)

        #run server
        self.Server_Button = QtWidgets.QPushButton(self.gridLayoutWidget, clicked = lambda : self.openWindow(ServerWindow))
        self.Server_Button.setFont(self.font)
        self.Server_Button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.Server_Button.setText('Run Server')
        self.gridLayout.addWidget(self.Server_Button,0,0,1,1)

        #restock
        self.Restock_Button = QtWidgets.QPushButton(self.gridLayoutWidget, clicked = lambda : self.openWindow(RestockWindow))
        self.Restock_Button.setFont(self.font)
        self.Restock_Button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.Restock_Button.setText('Restock')
        self.gridLayout.addWidget(self.Restock_Button,1,0,1,1)
        #------------------------------------------------------------

        #supplierbill
        self.Supplierbill_Button = QtWidgets.QPushButton(self.gridLayoutWidget, clicked = lambda : self.openWindow(SupplierbillWindow))
        self.Supplierbill_Button.setFont(self.font)
        self.Supplierbill_Button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.Supplierbill_Button.setText('Supplier bill')
        self.gridLayout.addWidget(self.Supplierbill_Button,2,0,1,1)
        #------------------------------------------------------------

        #Database
        self.Database_Button = QtWidgets.QPushButton(self.gridLayoutWidget, clicked = lambda : self.openWindow(DatabaseWindow))
        self.Database_Button.setFont(self.font)
        self.Database_Button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.Database_Button.setText('Data base')
        self.gridLayout.addWidget(self.Database_Button,3,0,1,1)
        #------------------------------------------------------------

        #quick stock check
        self.Quickcheck_Button = QtWidgets.QPushButton(self.gridLayoutWidget, clicked = lambda : self.openWindow(AlertWindow))
        self.Quickcheck_Button.setFont(self.font)
        self.Quickcheck_Button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.Quickcheck_Button.setText('Quick Stock Check')
        self.gridLayout.addWidget(self.Quickcheck_Button,4,0,1,1)
        #------------------------------------------------------------

        self.version_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.version_label.setAlignment(QtCore.Qt.AlignRight)
        self.font.setPointSize(16)
        self.version_label.setFont(self.font)
        self.version_label.setText('version : 2.0')
        self.gridLayout.addWidget(self.version_label,5,0,1,1)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
