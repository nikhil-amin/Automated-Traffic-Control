import sys
from PyQt5 import uic, QtWidgets, QtCore
import time
import threading

Ui_MainWindow, QtBaseClass = uic.loadUiType('GUI.ui')  # Loading GUI layout

TIMER_INIT = 0  # Initializing every lane's timer to 0


class MyApp(QtWidgets.QMainWindow):

    def __init__(self, rec_cap, dict_in_q, q_number_of_lanes):
        super(MyApp, self).__init__()
        self.dict_timer = dict_in_q
        self.number_of_lanes = q_number_of_lanes
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.TimeLeft1 = TIMER_INIT
        self.TimeLeft2 = TIMER_INIT
        self.TimeLeft3 = TIMER_INIT
        self.TimeLeft4 = TIMER_INIT  
        self.GUI_display()


    def displayGUI(self,my_dict_timer1,capacity1,numberOfLanes):
        
        my_dict_timer = my_dict_timer1
        capacity = capacity1


        # display capacity
        if numberOfLanes in [1,2,3,4]:
            self.ui.lineEdit_c1.setText(str(capacity[0]))
        else:
            self.ui.lineEdit_c1.setText("-NA-")
        if numberOfLanes in [2,3,4]:
            self.ui.lineEdit_c2.setText(str(capacity[1]))
        else:
            self.ui.lineEdit_c2.setText("-NA-")
        if numberOfLanes in [3,4]:
            self.ui.lineEdit_c3.setText(str(capacity[2]))
        else:
            self.ui.lineEdit_c3.setText("-NA-")
        if numberOfLanes == 4:
            self.ui.lineEdit_c4.setText(str(capacity[3]))
        else:
            self.ui.lineEdit_c4.setText("-NA-")


        # display timer
        if numberOfLanes in [1,2,3,4]:
            self.ui.lineEdit_t1.setText(str(my_dict_timer[capacity[0]]))
        else:
            self.ui.lineEdit_t1.setText(str(self.TimeLeft1))

        if numberOfLanes in [2,3,4]:
            self.ui.lineEdit_t2.setText(str(my_dict_timer[capacity[1]]))
        else:
            self.ui.lineEdit_t2.setText(str(self.TimeLeft2))
            
        if numberOfLanes in [3,4]:
            self.ui.lineEdit_t3.setText(str(my_dict_timer[capacity[2]]))
        else:
            self.ui.lineEdit_t3.setText(str(self.TimeLeft3))

        if numberOfLanes == 4:
            self.ui.lineEdit_t4.setText(str(my_dict_timer[capacity[3]]))
        else:
            self.ui.lineEdit_t4.setText(str(self.TimeLeft4))

        if numberOfLanes in [1,2,3,4]:
            self.TimeLeft1 = my_dict_timer[capacity[0]] +1
        if numberOfLanes in [2,3,4]:
            self.TimeLeft2 = my_dict_timer[capacity[1]] +1
        if numberOfLanes in [3,4]:
            self.TimeLeft3 = my_dict_timer[capacity[2]] +1
        if numberOfLanes == 4:
            self.TimeLeft4 = my_dict_timer[capacity[3]] +1

        self._updateTimer = QtCore.QTimer()
        self._updateTimer.timeout.connect(self.timeOut)
        self._updateTimer.start(1000)  


    # timer countdowns
    def timeOut(self):
        if self.TimeLeft1 != 0:
            self.TimeLeft1 -= 1
            self.ui.lineEdit_t1.setText(str(self.TimeLeft1)) 
        if self.TimeLeft1 == 0 and self.TimeLeft2 != 0:
            self.TimeLeft2 -= 1
            self.ui.lineEdit_t2.setText(str(self.TimeLeft2)) 
        if self.TimeLeft1 == 0 and self.TimeLeft2 == 0 and self.TimeLeft3 != 0:
            self.TimeLeft3 -= 1
            self.ui.lineEdit_t3.setText(str(self.TimeLeft3)) 
        if self.TimeLeft1 == 0 and self.TimeLeft2 == 0 and self.TimeLeft3 == 0 and self.TimeLeft4 != 0:
            self.TimeLeft4 -= 1
            self.ui.lineEdit_t4.setText(str(self.TimeLeft4))   
        if self.TimeLeft1 == 0 and self.TimeLeft2 == 0 and self.TimeLeft3 == 0 and self.TimeLeft4 == 0:
            numberOfLanes = self.number_of_lanes.get()
            my_dict_timer2 = self.dict_timer.get()
            capacity2 = list(my_dict_timer2.keys()) 
            self.displayGUI(my_dict_timer2,capacity2,numberOfLanes)


    def GUI_display(self):
        numberOfLanes = self.number_of_lanes.get()
        my_dict_timer = self.dict_timer.get()
        capacity = list(my_dict_timer.keys())
        self.displayGUI(my_dict_timer,capacity,numberOfLanes)

        
def mymain3(rec_cap,dict_in_q,q_number_of_lanes):
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp(rec_cap,dict_in_q,q_number_of_lanes)
    window.show()
    sys.exit(app.exec_())
