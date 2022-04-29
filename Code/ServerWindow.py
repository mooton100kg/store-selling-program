import threading
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from server import start
from socket import gethostname,gethostbyname

class Server_Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Server_Window, self).__init__()
        self.font = QtGui.QFont()
        self.font.setPointSize(16)
        self.setupUi()

    def setupUi(self):
        self.resize(100, 100)
        self.setMaximumSize(QtCore.QSize(100, 100))
        self.gridLayoutWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.gridLayoutWidget)
        self.main_gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)

        #IP Adress
        self.IP_Label = QtWidgets.QLabel( f'IP Adress : {gethostbyname(gethostname())}')
        self.IP_Label.setFont(self.font)
        self.main_gridLayout.addWidget(self.IP_Label, 0, 0, 1, 1)
        #-------------------------------------------------------------

        #Port
        self.P_Label = QtWidgets.QLabel('Port : 5050')
        self.P_Label.setFont(self.font)
        self.main_gridLayout.addWidget(self.P_Label, 1, 0, 1, 1)
        #-------------------------------------------------------------

        #Run
        self.Run_Button = QtWidgets.QPushButton( 'Run Server', clicked = lambda : self.start())
        self.Run_Button.setFont(self.font)
        self.main_gridLayout.addWidget(self.Run_Button, 2, 0, 1, 2)
        #-------------------------------------------------------------

        #Close
        self.Close_Button = QtWidgets.QPushButton( 'Close Server', clicked = lambda : self.stop())
        self.Close_Button.setFont(self.font)
        self.main_gridLayout.addWidget(self.Close_Button, 2, 0, 1, 2)
        self.Close_Button.hide()
        #-------------------------------------------------------------


    def stop(self):
        self.close()


    def start(self):
        self.Run_Button.hide()
        self.Close_Button.show()
        #creat threading for recieve data from server.py file
        self.run = threading.Thread(target=start)
        self.run.start()
        



        

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Server_Window()
    window.show()
    sys.exit(app.exec_())
    
