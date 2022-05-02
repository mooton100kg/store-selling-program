from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self,parent)
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(3)
        self.setCentralWidget(self.table)

        data1 = ['row1','row2','row3','row4']
        data2 = ['1','2.0','3.00000001','3.9999999']

        self.table.setRowCount(4)

        for index in range(4):
            item1 = QtWidgets.QTableWidgetItem(data1[index])
            self.table.setItem(index,0,item1)

            item2 = QtWidgets.QTableWidgetItem(data2[index])
            self.table.setItem(index,1,item2)
            
            self.btn_sell = QtWidgets.QPushButton('Edit')
            self.btn_sell.clicked.connect(self.handleButtonClicked)
            self.table.setCellWidget(index,2,self.btn_sell)

    def handleButtonClicked(self):
        button = QtWidgets.qApp.focusWidget()
        # or button = self.sender()
        index = self.table.indexAt(button.pos())
        if index.isValid():
            print(index.row(), index.column())



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())