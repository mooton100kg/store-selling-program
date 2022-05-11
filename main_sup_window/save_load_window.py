from PyQt5 import QtWidgets,QtCore, QtGui

from func import Save,Load

class SaveLoadWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(SaveLoadWindow, self).__init__()
        self.resize(675, 488)
        self.setFixedSize(300,100)
        self.font = QtGui.QFont()
        self.font.setPointSize(24)
        self.setupUi()


    def setupUi(self):
            self.gridLayoutWidget = QtWidgets.QWidget(self)
            self.setCentralWidget(self.gridLayoutWidget)
            self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)

            #save
            self.Save_Button = QtWidgets.QPushButton("Save data")
            self.Save_Button.setFont(self.font)
            self.Save_Button.clicked.connect(self.clicked_save)
            self.gridLayout.addWidget(self.Save_Button,0,0,1,1)
            #-----------------------------------------------------

            #load
            self.Save_Button = QtWidgets.QPushButton("Load data")
            self.Save_Button.setFont(self.font)
            self.Save_Button.clicked.connect(self.clicked_load)
            self.gridLayout.addWidget(self.Save_Button,1,0,1,1)
            #-----------------------------------------------------

    def clicked_load(self):
        fileName = QtWidgets.QFileDialog.getExistingDirectory(self,'Select Output Folder')
        if fileName:
            Load(fileName)
            self.close()

    def clicked_save(self):
        Save()
        self.close()


