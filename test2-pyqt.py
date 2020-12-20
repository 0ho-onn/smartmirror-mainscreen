#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# made by onips(0hoon)


from PyQt5 import QtCore, QtGui, QtWidgets    #pip install pyqt5(pip install python3-pyqt5)
import datetime       #get time
from time import sleep
import time
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
picNum = 0

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
        self.date.setGeometry(QtCore.QRect(30, 25, 350, 70))
        self.date.setObjectName("date")
        self.date.setFont(QtGui.QFont("",45))
        
        #time label
        self.time = QtWidgets.QLabel(self.centralwidget)
        self.time.setGeometry(QtCore.QRect(30, 100, 350, 50))
        self.time.setObjectName("time")
        self.time.setFont(QtGui.QFont("",35))
        #-------------------------------------------------------------------------
        #weather label
        self.weather = QtWidgets.QLabel(self.centralwidget)
        self.weather.setGeometry(QtCore.QRect(900, 5, 100, 90))
        self.weather.setObjectName("weather")
        
        #temp label
        self.temp = QtWidgets.QLabel(self.centralwidget)
        self.temp.setGeometry(QtCore.QRect(850, 90, 330, 50))
        self.temp.setObjectName("temp")
        self.temp.setFont(QtGui.QFont("",30))
        #-------------------------------------------------------------------------
        #cam view point
        self.camview = QtWidgets.QLabel(self.centralwidget)
        self.camview.setGeometry(QtCore.QRect(0, 300, 1600, 1200))
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
        self.btn_start.setGeometry(QtCore.QRect(500, 1700, 91, 61))
        self.btn_start.setObjectName("btn_start")
        #-------------------------------------------------------------------------
        #clothes save button
        self.cloth_save = QtWidgets.QPushButton(self.centralwidget)
        self.cloth_save.setGeometry(QtCore.QRect(80, 1700, 91, 61))
        self.cloth_save.setObjectName("cloth_save")
        
        #clothes save success
        self.save_success = QtWidgets.QLabel(self.centralwidget)
        self.save_success.setGeometry(QtCore.QRect(300, 750, 700, 300))
        self.save_success.setObjectName("save_success")
        self.save_success.setFont(QtGui.QFont("",50))
        #-------------------------------------------------------------------------
        #clothes list button
        self.btn_list = QtWidgets.QPushButton(self.centralwidget)
        self.btn_list.setGeometry(QtCore.QRect(900, 1700, 91, 61))
        self.btn_list.setObjectName("btn_list")
        #-------------------------------------------------------------------------
        #list layout
        self.label1 = QtWidgets.QLabel(self.centralwidget)
        self.label1.setGeometry(QtCore.QRect(140, 150, 300, 300))
        self.label1.setObjectName("label1")
        
        self.label2 = QtWidgets.QLabel(self.centralwidget)
        self.label2.setGeometry(QtCore.QRect(470, 150, 300, 300))
        self.label2.setObjectName("label2")
        
        self.label3 = QtWidgets.QLabel(self.centralwidget)
        self.label3.setGeometry(QtCore.QRect(800, 150, 300, 300))
        self.label3.setObjectName("label3")
        
        self.label4 = QtWidgets.QLabel(self.centralwidget)
        self.label4.setGeometry(QtCore.QRect(140, 350, 300, 300))
        self.label4.setObjectName("label4")
        
        self.label5 = QtWidgets.QLabel(self.centralwidget)
        self.label5.setGeometry(QtCore.QRect(470, 350, 300, 300))
        self.label5.setObjectName("label5")
        
        self.label6 = QtWidgets.QLabel(self.centralwidget)
        self.label6.setGeometry(QtCore.QRect(800, 350, 300, 300))
        self.label6.setObjectName("label6")
        
        self.label7 = QtWidgets.QLabel(self.centralwidget)
        self.label7.setGeometry(QtCore.QRect(140, 550, 300, 300))
        self.label7.setObjectName("label7")
        
        self.label8 = QtWidgets.QLabel(self.centralwidget)
        self.label8.setGeometry(QtCore.QRect(470, 550, 300, 300))
        self.label8.setObjectName("label8")
        
        self.label9 = QtWidgets.QLabel(self.centralwidget)
        self.label9.setGeometry(QtCore.QRect(800, 550, 300, 300))
        self.label9.setObjectName("label9")
        
        
        
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
        
        self.save_success.setText(_translate("MainWindow", "save complete"))
        self.save_success.hide()

        
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
            elif (now.hour == 12):
                hour = 12
            else:
                AmOrPm = "AM"
                
            if (int(hour) < 10):
                hour = "0" + str(hour)
            if (int(minute) < 10):
                minute = "0" + str(minute)
            
            self.date.setText("%s/%s/%s" %(now.year, now.month, now.day))
            self.time.setText("%s : %s " %(hour, minute)+AmOrPm)
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
        print(weather +" " + temp)
        
        #request weather icon
        data = urllib.request.urlopen("http://openweathermap.org/img/wn/02d@2x.png").read()  #%s to 10d vision
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        self.weather.setPixmap(pixmap)
        self.weather.show()
        
        self.temp.setText("Asan / %s℃ " %(temp))
        
    #show cam function
    def show_camera(self, MainWindow):
        global running        #running for cam off ***(not yet)***
        global img
        
        cam = cv2.VideoCapture(0)
        
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1600)    #set camera view size
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1200)
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
            
            #if (isSave == 1):
                
                    
        cam.release()
        print("Thread end.")
        
    #image save function
    def save_image(self, MainWindow):
        global img
        global picNum
        
        picNum = picNum + 1
        
        cv2.imwrite("./clothes/%s.png" %(picNum), img, params=[cv2.IMWRITE_PNG_COMPRESSION, 0])
        self.save_success.show()
        time.sleep(2)
        self.save_success.hide()
        
    #list show function
    def list_show(self, MainWindow):
        global isHide
        
        pixmap = QPixmap("./clothes/1.png")
        pixmap = pixmap.scaledToWidth(300)
        self.label1.setPixmap(QPixmap(pixmap))
        self.label1.hide()
        
        pixmap2 = QPixmap("./clothes/2.png")
        pixmap2 = pixmap2.scaledToWidth(300)
        self.label2.setPixmap(QPixmap(pixmap2))
        self.label2.hide()
        
        pixmap3 = QPixmap("./clothes/3.png")
        pixmap3 = pixmap3.scaledToWidth(300)
        self.label3.setPixmap(QPixmap(pixmap3))
        self.label3.hide()
        
        pixmap4 = QPixmap("./clothes/4.png")
        pixmap4 = pixmap4.scaledToWidth(300)
        self.label4.setPixmap(QPixmap(pixmap4))
        self.label4.hide()
        
        pixmap5 = QPixmap("./clothes/5.png")
        pixmap5 = pixmap5.scaledToWidth(300)
        self.label5.setPixmap(QPixmap(pixmap5))
        self.label5.hide()
        
        pixmap6 = QPixmap("./clothes/6.png")
        pixmap6 = pixmap6.scaledToWidth(300)
        self.label6.setPixmap(QPixmap(pixmap6))
        self.label6.hide()
        
        pixmap7 = QPixmap("./clothes/7.png")
        pixmap7 = pixmap7.scaledToWidth(300)
        self.label7.setPixmap(QPixmap(pixmap7))
        self.label7.hide()
        
        pixmap8 = QPixmap("./clothes/8.png")
        pixmap8 = pixmap8.scaledToWidth(300)
        self.label8.setPixmap(QPixmap(pixmap8))
        self.label8.hide()
        
        pixmap9 = QPixmap("./clothes/9.png")
        pixmap9 = pixmap9.scaledToWidth(300)
        self.label9.setPixmap(QPixmap(pixmap9))
        self.label9.hide()
        
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
    
    def imgSave_start(self, MainWindow):
        thread = threading.Thread(target=self.save_image, args=(self,))
        thread.daemon = True
        thread.start()
    
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
    ui.cloth_save.clicked.connect(lambda: ui.imgSave_start(MainWindow))
    ui.btn_list.clicked.connect(lambda: ui.list_start(MainWindow))
    
    MainWindow.show()
    sys.exit(app.exec_())

