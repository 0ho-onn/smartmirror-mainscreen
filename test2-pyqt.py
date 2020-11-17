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
        #clothes list button
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(1100, 900, 91, 61))
        self.pushButton_2.setObjectName("pushButton_2")
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
        self.btn_start.setText(_translate("MainWindow", "clothes save"))
        self.pushButton_2.setText(_translate("MainWindow", "PushButton"))
        
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
                hour = "0" + str(hour);
            if (now.minute < 10):
                minute = "0" + str(minute);
            else:
                AmOrPm = "AM"

            self.date.setText("%sY %sM %sD" %(now.year, now.month, now.day))
            self.time.setText(AmOrPm+" %s : %s" %(hour, minute))
            sleep(1)
    
    #weather function
    def set_weather(self, MainWindow):
        #request openweathermap site for weather&teamperature
        reqForWeather = urllib.request.Request("http://api.openweathermap.org/data/2.5/weather?q=Cheonan&units=metric&appid=f611edc8235273d9f945d6229d31186e")
        weatherData = urllib.request.urlopen(reqForWeather).read()
        dataFile = open("./weatherData.json", mode="w", encoding='utf-8')
        data_str = str(weatherData, "utf-8")
        dataFile.write(str(data_str))
        dataFile.close()
        config = readConfig('weatherData.json')
        weather = config['weather'][0]['icon']
        temp = str(config['main']['temp'])
        #print(weather +" " + temp)
        
        #request weather icon
        data = urllib.request.urlopen("http://openweathermap.org/img/wn/%s@2x.png" %(weather)).read()  #%s to 10d vision
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        self.weather.setPixmap(pixmap)
        self.weather.show()
        
        self.temp.setText("temp : %s " %(temp))
        
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
    
    MainWindow.show()
    sys.exit(app.exec_())

