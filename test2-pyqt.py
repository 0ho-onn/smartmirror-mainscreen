# -*- coding: utf-8 -*-
# made by onips(0hoon)

from PyQt5 import QtCore, QtGui, QtWidgets    #pip install pyqt5(pip install python3-pyqt5)
import datetime       #get time
from time import sleep
import threading
import tkinter as tk    #python GUI programing?
import urllib.request   #this for weather api url
import requests
import json
import cv2     #opencv
from PyQt5.QtGui import QPixmap, QImage  #use image in Python 

#for camera prototype
running = True
#for list
isHide = 0
#read stream for weather
def readConfig(filename):
    global json
    file = open(filename, "r", encoding="utf-8")
    json = (json.loads(file.read()))
    file.close()
    return json

class Ui_MainWindow(object):
    hello_world = 0
    root = tk.Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    start_or_stop = False
    start = True
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        
        palette = QtGui.QPalette()
        #text to white
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        #background to black
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)

        MainWindow.setPalette(palette)
        MainWindow.showFullScreen()
        
        #-------------------------------------------------------------------------
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        #-------------------------------------------------------------------------
        #date label
        self.date = QtWidgets.QLabel(self.centralwidget)
        self.date.setGeometry(QtCore.QRect(30, 25, 320, 50))
        self.date.setObjectName("date")
        self.date.setFont(QtGui.QFont("",30))
        
        #time label
        self.time = QtWidgets.QLabel(self.centralwidget)
        self.time.setGeometry(QtCore.QRect(30, 90, 320, 31))
        self.time.setObjectName("time")
        self.time.setFont(QtGui.QFont("",20))
        #-------------------------------------------------------------------------
        #weather label
        self.weather = QtWidgets.QLabel(self.centralwidget)
        self.weather.setGeometry(QtCore.QRect(1130, 5, 100, 90))
        self.weather.setObjectName("weather")
        
        #temp label
        self.temp = QtWidgets.QLabel(self.centralwidget)
        self.temp.setGeometry(QtCore.QRect(1100, 100, 300, 20))
        self.temp.setObjectName("temp")
        self.temp.setFont(QtGui.QFont("",15))
        #-------------------------------------------------------------------------
        #cam view point
        self.camview = QtWidgets.QLabel(self.centralwidget)
        self.camview.setGeometry(QtCore.QRect(0, 150, 1100, 700))
        self.camview.setObjectName("camview")
        
        #cam view scroll area
        #self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        #self.scrollArea.setGeometry(QtCore.QRect(90, 150, 1100, 700))
        #self.scrollArea.setWidgetResizable(True)
        #self.scrollArea.setObjectName("scrollArea")
        #self.scrollAreaWidgetContents = QtWidgets.QWidget()
        #self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1100, 700))
        #self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        #self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        #-------------------------------------------------------------------------
        #clothes save button
        self.btn_start = QtWidgets.QPushButton(self.centralwidget)
        self.btn_start.setGeometry(QtCore.QRect(570, 900, 91, 61))
        self.btn_start.setObjectName("btn_start")
        #-------------------------------------------------------------------------
        #clothes save button
        self.cloth_save = QtWidgets.QPushButton(self.centralwidget)
        self.cloth_save.setGeometry(QtCore.QRect(80, 900, 91, 61))
        self.cloth_save.setObjectName("cloth_save")
        #-------------------------------------------------------------------------
        #clothes list button
        self.btn_list = QtWidgets.QPushButton(self.centralwidget)
        self.btn_list.setGeometry(QtCore.QRect(1100, 900, 91, 61))
        self.btn_list.setObjectName("btn_list")
        #-------------------------------------------------------------------------
        #list layout
        self.label1 = QtWidgets.QLabel(self.centralwidget)
        self.label1.setGeometry(QtCore.QRect(200, 100, 300, 300))
        self.label1.setObjectName("label1")
        
        self.label2 = QtWidgets.QLabel(self.centralwidget)
        self.label2.setGeometry(QtCore.QRect(500, 100, 300, 300))
        self.label2.setObjectName("label2")
        
        self.label3 = QtWidgets.QLabel(self.centralwidget)
        self.label3.setGeometry(QtCore.QRect(800, 100, 300, 300))
        self.label3.setObjectName("label3")
        
        self.label4 = QtWidgets.QLabel(self.centralwidget)
        self.label4.setGeometry(QtCore.QRect(200, 400, 300, 300))
        self.label4.setObjectName("label4")
        
        self.label5 = QtWidgets.QLabel(self.centralwidget)
        self.label5.setGeometry(QtCore.QRect(500, 400, 300, 300))
        self.label5.setObjectName("label5")
        
        self.label6 = QtWidgets.QLabel(self.centralwidget)
        self.label6.setGeometry(QtCore.QRect(800, 400, 300, 300))
        self.label6.setObjectName("label6")
        
        self.label7 = QtWidgets.QLabel(self.centralwidget)
        self.label7.setGeometry(QtCore.QRect(200, 700, 300, 300))
        self.label7.setObjectName("label7")
        
        self.label8 = QtWidgets.QLabel(self.centralwidget)
        self.label8.setGeometry(QtCore.QRect(500, 700, 300, 300))
        self.label8.setObjectName("label8")
        
        self.label9 = QtWidgets.QLabel(self.centralwidget)
        self.label9.setGeometry(QtCore.QRect(800, 700, 300, 300))
        self.label9.setObjectName("label9")
        
        pixmap = QPixmap("./clothes/images.jpeg")
        self.label1.setPixmap(QPixmap(pixmap))
        self.label1.hide()
        
        pixmap = QPixmap("./clothes/images.jpeg")
        self.label2.setPixmap(QPixmap(pixmap))
        self.label2.hide()
        
        pixmap = QPixmap("./clothes/images.jpeg")
        self.label3.setPixmap(QPixmap(pixmap))
        self.label3.hide()
        
        pixmap = QPixmap("./clothes/images.jpeg")
        self.label4.setPixmap(QPixmap(pixmap))
        self.label4.hide()
        
        pixmap = QPixmap("./clothes/images.jpeg")
        self.label5.setPixmap(QPixmap(pixmap))
        self.label5.hide()
        
        pixmap = QPixmap("./clothes/images.jpeg")
        self.label6.setPixmap(QPixmap(pixmap))
        self.label6.hide()
        
        pixmap = QPixmap("./clothes/images.jpeg")
        self.label7.setPixmap(QPixmap(pixmap))
        self.label7.hide()
        
        pixmap = QPixmap("./clothes/images.jpeg")
        self.label8.setPixmap(QPixmap(pixmap))
        self.label8.hide()
        
        pixmap = QPixmap("./clothes/images.jpeg")
        self.label9.setPixmap(QPixmap(pixmap))
        self.label9.hide()
        
        #-------------------------------------------------------------------------
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        #-------------------------------------------------------------------------
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        #self.time.setText(_translate("MainWindow", "time"))
        #self.temp.setText(_translate("MainWindow", "weather info"))
        #self.weather.setText(_translate("MainWindow", "weather info"))
        self.btn_start.setText(_translate("MainWindow", "camera start"))
        self.cloth_save.setText(_translate("MainWindow", "clothes save"))
        self.btn_list.setText(_translate("MainWindow", "clothes list"))

        
        #-------------------------------------------------------------------------
        #function coding
    #time function
    def set_time(self, MainWindow):
        AmOrPm = "AM"
        while True:
            now = datetime.datetime.now()
            hour = now.hour
            minute = now.minute
            
            #time view like clock
            if (now.hour >= 12):
                AmOrPm = "PM"
                hour = now.hour % 12
            if (now.hour == 12):
                hour = 12
            if (now.hour < 10):
                hour = "0" + str(hour)
            if (now.minute < 10):
                minute = "0" + str(minute)
            else:
                AmOrPm = "AM"

            self.date.setText("%sY %sM %sD" %(now.year, now.month, now.day))
            self.time.setText(AmOrPm+" %s : %s" %(hour, minute))
            sleep(1)
    
    #weather function
    def set_weather(self, MainWindow):
        #request openweathermap site for weather&teamperature
        reqForWeather = urllib.request.Request("http://api.openweathermap.org/data/2.5/weather?q=Asan&units=metric&appid=f611edc8235273d9f945d6229d31186e")
        weatherData = urllib.request.urlopen(reqForWeather).read()
        dataFile = open("./weatherData.json", mode="w", encoding='utf-8')
        data_str = str(weatherData, "utf-8")
        dataFile.write(str(data_str))
        dataFile.close()
        config = readConfig('weatherData.json')
        weather = config['weather'][0]['icon']
        temp = str(round(config['main']['temp']))
        #print(weather +" " + temp)
        
        #request weather icon
        data = urllib.request.urlopen("http://openweathermap.org/img/wn/%s@2x.png" %(weather)).read()  #%s to 10d vision
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        self.weather.setPixmap(pixmap)
        self.weather.show()
        
        self.temp.setText("Asan / %s℃ " %(temp))
        
    #show cam function
    def show_camera(self, MainWindow):
        global running        #running for cam off ***(not yet)***
        
        cam = cv2.VideoCapture(0)
        
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)    #set camera view size
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        width = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.camview.resize(width, height)
        
        while running:
            ret, img = cam.read()
            if ret:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
                h,w,c = img.shape
                qImg = QtGui.QImage(img.data, w, h, w*c, QtGui.QImage.Format_RGB888)
                pixmap = QtGui.QPixmap.fromImage(qImg)
                self.camview.setPixmap(pixmap)
            else:
                QtWidgets.QMessageBox.about(win, "Error", "Cannot read frame.")
                print("cannot read frame.")
                break
        cam.release()
        print("Thread end.")
        
        
    #image save function
    #def save_image(self, MainWindow):
     #   save_img = cv2.imread(image)
     #   cv2.imwrite('1.jpg', save_img)
        
    #list show function
    def list_show(self, MainWindow):
        global isHide
        
        if (isHide == 0):
            self.label1.show()
            self.label2.show()
            self.label3.show()
            self.label4.show()
            self.label5.show()
            self.label6.show()
            self.label7.show()
            self.label8.show()
            self.label9.show()
            isHide = 1
        else:
            self.label1.hide()
            self.label2.hide()
            self.label3.hide()
            self.label4.hide()
            self.label5.hide()
            self.label6.hide()
            self.label7.hide()
            self.label8.hide()
            self.label9.hide()
            isHide = 0
        
        
    #-------------------------------------------------------------------------
    #threads
            
    #time thread
    def time_start(self, MainWindow):
        thread = threading.Thread(target=self.set_time, args=(self,))
        thread.daemon = True
        thread.start()
    #weather thread
    def weather_start(self, MainWindow):
        thread = threading.Thread(target=self.set_weather, args=(self,))
        thread.daemon = True
        thread.start()
    #camShow thread
    def cam_start(self, MainWindow):
        thread = threading.Thread(target=self.show_camera, args=(self,))
        thread.daemon = True
        thread.start()
    
    #def imgSave_start(self, MainWindow):
     #   thread = threading.Thread(target=self.save_image, args=(self,))
     #   thread.daemon = True
     #   thread.start()
    
    def list_start(self, MainWindow):
        thread = threading.Thread(target=self.list_show, args=(self,))
        thread.daemon = True
        thread.start()
    #-------------------------------------------------------------------------
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    
    #threads
    ui.time_start(MainWindow) #time thread
    ui.weather_start(MainWindow)
    #ui.cam_start(MainWindow)
    ui.btn_start.clicked.connect(lambda: ui.cam_start(MainWindow))    #lambda for use arg
    #ui.btn_start.clicked.connect(lambda: ui.imgSave_start(MainWindow))
    ui.btn_list.clicked.connect(lambda: ui.list_start(MainWindow))
    
    MainWindow.show()
    sys.exit(app.exec_())

