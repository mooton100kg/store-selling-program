from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd
from datetime import date,timedelta,datetime


class Sellprofit_Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Sellprofit_Window, self).__init__()
        self.font = QtGui.QFont()
        self.font.setPointSize(16)
        self.input_info = pd.read_csv('Total_sell.csv', dtype=str).to_dict('list')
        self.df = pd.read_csv('Total_sell.csv', dtype=str)
        self.setupUi()

    def profit_today(self):
        today = date.today().strftime('%d')
        yesterday = (date.today() - timedelta(days=1)).strftime('%d')
        my = date.today().strftime('%m-%y')

        if today in self.input_info['today'] and my in self.input_info['month_year']:
            row = self.df.query(f'today == "{today}" and month_year == "{my}"').index[0]
            p_today = int(self.input_info['selltoday'][row]) - int(self.input_info['costtoday'][row])
            p_yesterday = int(self.input_info['sellyesterday'][row]) - int(self.input_info['costyesterday'][row])
        
        elif today not in self.input_info['today'] and yesterday in self.input_info['today'] and my in self.input_info['month_year']:
            row = self.df.query(f'today == "{yesterday}" and month_year == "{my}"').index[0]
            p_today = 'none'
            p_yesterday = int(self.input_info['selltoday'][row]) - int(self.input_info['costtoday'][row])
        
        elif today not in self.input_info['today'] or my not in self.input_info['month_year']:
            p_today = 'none'
            p_yesterday = 'none'

        return [p_today,p_yesterday]

    def profit_month(self,year: str = date.today().strftime('%y')):
        if year in [year.split('-')[1] for year in self.input_info['month_year']]:
            my = [m+'-'+year for m in ['01','02','03','04','05','06','07','08','09','10','11','12']]
            P_month = []
            P_year = []
            for m_y in my:
                if m_y in self.input_info['month_year']:
                    row = self.input_info['month_year'].index(m_y)
                    p_m = int(self.input_info['sellallmonth'][row]) - int(self.input_info['costallmonth'][row])
                    P_year.append(int(p_m))
                elif m_y not in self.input_info['month_year']:
                    p_m = 'none'
                P_month.append(str(p_m))

            return P_month,sum(P_year)


    def setupUi(self):
        self.resize(200, 400)
        self.move(20,20)
        self.gridLayoutWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.gridLayoutWidget)
        self.main_gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)

        #Day
        p = self.profit_today()
        self.Day_Label = QtWidgets.QLabel(f'Today : {p[0]}')
        self.Day_Label.setFont(self.font)
        self.main_gridLayout.addWidget(self.Day_Label,0,0,1,1)

        self.Yesterday_Label = QtWidgets.QLabel(f'Yesterday : {p[1]}')
        self.Yesterday_Label.setFont(self.font)
        self.main_gridLayout.addWidget(self.Yesterday_Label,0,1,1,1)
        #---------------------------------------------------------------
   
        #Month
        p,py = self.profit_month()
        self.Jan_Label = QtWidgets.QLabel(f'ม.ค. : {p[0]}')
        self.Jan_Label.setFont(self.font)
        self.main_gridLayout.addWidget(self.Jan_Label,1,0,1,1)

        self.Feb_Label = QtWidgets.QLabel(f'ก.พ. : {p[1]}')
        self.Feb_Label.setFont(self.font)
        self.main_gridLayout.addWidget(self.Feb_Label,2,0,1,1)

        self.Mar_Label = QtWidgets.QLabel(f'มี.ค. : {p[2]}')
        self.Mar_Label.setFont(self.font)
        self.main_gridLayout.addWidget(self.Mar_Label,3,0,1,1)

        self.Api_Label = QtWidgets.QLabel(f'เม.ย. : {p[3]}')
        self.Api_Label.setFont(self.font)
        self.main_gridLayout.addWidget(self.Api_Label,4,0,1,1)

        self.May_Label = QtWidgets.QLabel(f'พ.ค. : {p[4]}')
        self.May_Label.setFont(self.font)
        self.main_gridLayout.addWidget(self.May_Label,5,0,1,1)

        self.Jun_Label = QtWidgets.QLabel(f'มิ.ย. : {p[5]}')
        self.Jun_Label.setFont(self.font)
        self.main_gridLayout.addWidget(self.Jun_Label,6,0,1,1)

        self.Jul_Label = QtWidgets.QLabel(f'ก.ค. : {p[6]}')
        self.Jul_Label.setFont(self.font)
        self.main_gridLayout.addWidget(self.Jul_Label,1,1,1,1)

        self.Aus_Label = QtWidgets.QLabel(f'ส.ค. : {p[7]}')
        self.Aus_Label.setFont(self.font)
        self.main_gridLayout.addWidget(self.Aus_Label,2,1,1,1)

        self.Sep_Label = QtWidgets.QLabel(f'ก.ย. : {p[8]}')
        self.Sep_Label.setFont(self.font)
        self.main_gridLayout.addWidget(self.Sep_Label,3,1,1,1)

        self.Oct_Label = QtWidgets.QLabel(f'ต.ค. : {p[9]}')
        self.Oct_Label.setFont(self.font)
        self.main_gridLayout.addWidget(self.Oct_Label,4,1,1,1)

        self.Nov_Label = QtWidgets.QLabel(f'พ.ย. : {p[10]}')
        self.Nov_Label.setFont(self.font)
        self.main_gridLayout.addWidget(self.Nov_Label,5,1,1,1)

        self.Dec_Label = QtWidgets.QLabel(f'ธ.ค. : {p[11]}')
        self.Dec_Label.setFont(self.font)
        self.main_gridLayout.addWidget(self.Dec_Label,6,1,1,1)
        #---------------------------------------------------------------

        #year
        self.Year_Combobox = QtWidgets.QComboBox()
        self.Year_Combobox.setFont(self.font)
        y = list(set(['ปี '+datetime.strptime(year.split('-')[1], '%y').strftime('%Y') for year in self.input_info['month_year']]))
        self.Year_Combobox.addItems(y)
        self.Year_Combobox.setCurrentText('ปี '+date.today().strftime('%Y'))
        self.Year_Combobox.currentTextChanged.connect(self.changeyear)
        self.main_gridLayout.addWidget(self.Year_Combobox,7,0,1,1)

        self.Year_Label = QtWidgets.QLabel(f' : {str(py)}')
        self.Year_Label.setFont(self.font)
        self.main_gridLayout.addWidget(self.Year_Label,7,1,1,1)
        #---------------------------------------------------------------

    def changeyear(self):
        y = self.Year_Combobox.currentText()[-2:]
        p,py = self.profit_month(y)
        self.Jan_Label.setText(f'ม.ค. : {p[0]}')
        self.Feb_Label.setText(f'ก.พ. : {p[1]}')
        self.Mar_Label.setText(f'มี.ค. : {p[2]}')
        self.Api_Label.setText(f'เม.ย. : {p[3]}')
        self.May_Label.setText(f'พ.ค. : {p[4]}')
        self.Jun_Label.setText(f'มิ.ย. : {p[5]}')
        self.Jul_Label.setText(f'ก.ค. : {p[6]}')
        self.Aus_Label.setText(f'ส.ค. : {p[7]}')
        self.Sep_Label.setText(f'ก.ย. : {p[8]}')
        self.Oct_Label.setText(f'ต.ค. : {p[9]}')
        self.Nov_Label.setText(f'พ.ย. : {p[10]}')
        self.Dec_Label.setText(f'ธ.ค. : {p[11]}')
        self.Year_Label.setText(f' : {str(py)}')



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication([])
    window = Sellprofit_Window()
    window.show()
    sys.exit(app.exec_())
