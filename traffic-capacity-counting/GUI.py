import sys
from PyQt5 import uic, QtWidgets, QtCore
import time

Ui_MainWindow, QtBaseClass = uic.loadUiType('GUI.ui')

class MyApp(QtWidgets.QMainWindow):
    def __init__(self, rec_cap, dict_in_q):
        super(MyApp, self).__init__()
        # self.in_queue = rec_cap
        self.dict_timer = dict_in_q
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # self.TimeLeft=50
        self.ui.pushButton_start.clicked.connect(self.GUI_display)

    # def displayTimer(self):
    #     self.TimeLeft = 100
         
    #     self._updateTimer = QtCore.QTimer()
    #     self._updateTimer.timeout.connect(self.timeOut)
    #     self._updateTimer.start(1000)  

    # def timeOut(self):
    #     self.TimeLeft -= 1
    #     if self.TimeLeft == 0:
    #         self.TimeLeft = 0
    #     self.ui.lineEdit_t1.setText(str(self.TimeLeft))        

    def GUI_display(self):
        my_dict_timer = self.dict_timer.get()
        capacity = list(my_dict_timer.keys())

        # self.displayTimer()

        self.ui.lineEdit_c1.setText(str(capacity[0]))
        self.ui.lineEdit_c2.setText(str(capacity[1]))
        self.ui.lineEdit_c3.setText(str(capacity[2]))
        self.ui.lineEdit_c4.setText(str(capacity[3]))

        self.ui.lineEdit_t1.setText(str(my_dict_timer[capacity[0]]))
        self.ui.lineEdit_t2.setText(str(my_dict_timer[capacity[1]]))
        self.ui.lineEdit_t3.setText(str(my_dict_timer[capacity[2]]))
        self.ui.lineEdit_t4.setText(str(my_dict_timer[capacity[3]]))

        self._updateTimer = QtCore.QTimer()
        self._updateTimer.timeout.connect(self.GUI_display)
        self._updateTimer.start()   
        
        
def mymain3(rec_cap,dict_in_q):
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp(rec_cap,dict_in_q)
    window.show()
    sys.exit(app.exec_())
