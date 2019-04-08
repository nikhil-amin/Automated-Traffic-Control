import sys
from PyQt5 import uic, QtWidgets, QtCore, QtGui
import time
import threading
import cv2

Ui_MainWindow, QtBaseClass = uic.loadUiType('GUI.ui')  # Loading GUI layout

TIMER_INIT = 0  # Initializing every lane's timer to 0
running = False

class OwnImageWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(OwnImageWidget, self).__init__(parent)
        self.image = None

    def setImage(self, image):
        self.image = image
        sz = image.size()
        self.setMinimumSize(sz)
        self.update()

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        if self.image:
            qp.drawImage(QtCore.QPoint(0, 0), self.image)
        qp.end()

class MyApp(QtWidgets.QMainWindow):

    def __init__(self, rec_cap, dict_in_q, q_number_of_lanes, q_camera_frames):
        super(MyApp, self).__init__()
        self.dict_timer = dict_in_q
        self.number_of_lanes = q_number_of_lanes
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.TimeLeft1 = TIMER_INIT
        self.TimeLeft2 = TIMER_INIT
        self.TimeLeft3 = TIMER_INIT
        self.TimeLeft4 = TIMER_INIT  

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.timeOut)
        self.timer.start(1000)

        self.q_camera_frames = q_camera_frames
        self.window_width = self.ui.ImgWidget.frameSize().width()
        self.window_height = self.ui.ImgWidget.frameSize().height()
        self.ImgWidget = OwnImageWidget(self.ui.ImgWidget)


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
            self.TimeLeft1 = my_dict_timer[capacity[0]] +1
        else:
            self.ui.lineEdit_t1.setText(str(TIMER_INIT))

        if numberOfLanes in [2,3,4]:
            self.ui.lineEdit_t2.setText(str(my_dict_timer[capacity[1]]))
            self.TimeLeft2 = my_dict_timer[capacity[1]] +1
        else:
            self.ui.lineEdit_t2.setText(str(TIMER_INIT))
            
        if numberOfLanes in [3,4]:
            self.ui.lineEdit_t3.setText(str(my_dict_timer[capacity[2]]))
            self.TimeLeft3 = my_dict_timer[capacity[2]] +1
        else:
            self.ui.lineEdit_t3.setText(str(TIMER_INIT))

        if numberOfLanes == 4:
            self.ui.lineEdit_t4.setText(str(my_dict_timer[capacity[3]]))
            self.TimeLeft4 = my_dict_timer[capacity[3]] +1
        else:
            self.ui.lineEdit_t4.setText(str(TIMER_INIT))

        self._updateTimer = QtCore.QTimer()
        self._updateTimer.timeout.connect(self.update_frame)
        self._updateTimer.start(1)  


    #Camera Display
    def update_frame(self):
        if not self.q_camera_frames.empty():
            self.ui.pushButton_start.setText('Lane 1 Camera is LIVE')
            frame = self.q_camera_frames.get()
            img = frame["frame"]

            img_height, img_width, img_colors = img.shape
            scale_w = float(self.window_width) / float(img_width)
            scale_h = float(self.window_height) / float(img_height)
            scale = min([scale_w, scale_h])

            if scale == 0:
                scale = 1
            
            img = cv2.resize(img, None, fx=scale, fy=scale, interpolation = cv2.INTER_CUBIC)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            height, width, bpc = img.shape
            bpl = bpc * width
            image = QtGui.QImage(img.data, width, height, bpl, QtGui.QImage.Format_RGB888)
            self.ImgWidget.setImage(image)


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
            my_dict_timer2 = self.dict_timer.get()
            capacity2 = list(my_dict_timer2.keys()) 
            numberOfLanes = self.number_of_lanes.get()
            self.displayGUI(my_dict_timer2,capacity2,numberOfLanes)


    def GUI_display(self):

        numberOfLanes = self.number_of_lanes.get()
        my_dict_timer = self.dict_timer.get()
        capacity = list(my_dict_timer.keys())
        self.displayGUI(my_dict_timer,capacity,numberOfLanes)

        
def mymain3(rec_cap,dict_in_q,q_number_of_lanes,q_camera_frames):
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp(rec_cap,dict_in_q,q_number_of_lanes,q_camera_frames)
    window.show()
    sys.exit(app.exec_())
