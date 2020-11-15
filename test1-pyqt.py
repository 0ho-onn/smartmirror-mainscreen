# -*- coding: utf-8 -*- edit by onips(0hoon)

from PyQt5 import QtCore, QtGui, QtWidgets #pip install pyqt5(pip install python3-pyqt5)
import datetime       #get time
from time import sleep
import threading
import tkinter as tk #this can't pip install #python GUI programing?
import urllib.request #this for weather api url
import requests
import json
#import cv2     #opencv
from PyQt5.QtGui import QPixmap, QImage  #use image in Python 

#==================================================================================================
#==============UI_MAIN==============================================================================
#==================================================================================================

class Ui_MainWindow(object):
    hello_world = 0
    root = tk.Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    start_or_stop=False
    start=True

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")

        palette = QtGui.QPalette()

        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)

        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)

        MainWindow.setPalette(palette)
        #MainWindow.resize(800, 600)
        MainWindow.showFullScreen()

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        #날씨 이모티콘 ====================================================================
        self.weather = QtWidgets.QLabel(self.centralwidget)
        self.weather.setGeometry(QtCore.QRect(20, 15, 150,130))
        self.weather.setObjectName("weather")

        #온도 label [온도 출력]
        self.temperature = QtWidgets.QLabel(self.centralwidget)
        self.temperature.setGeometry(QtCore.QRect(25, 120, 150,130))
        self.temperature.setObjectName("temperature")
        self.temperature.setFont(QtGui.QFont("맑은 고딕",20))

        #================================================================================
        #clock 이라는 이름으로 label 생성 [hello world]===================================
        self.clock = QtWidgets.QLabel(self.centralwidget)
        self.clock.setGeometry(QtCore.QRect(200,300,100,50))
        self.clock.setObjectName("clock")

        #time 이라는 이름으로 label 생성 [(오전/오후)시/분]
        self.time = QtWidgets.QLabel(self.centralwidget)
        self.time.setGeometry(QtCore.QRect(170,80,800,60))
        self.time.setObjectName("time")
        #setFont(QtGui.QFont("Font_name",Font_size))
        self.time.setFont(QtGui.QFont("맑은 고딕",50)) 

        #date 이라는 이름으로 label 생성 [년/월/일]
        self.date = QtWidgets.QLabel(self.centralwidget)
        self.date.setGeometry(QtCore.QRect(180, 15, 300, 50))
        self.date.setObjectName("date")
        self.date.setFont(QtGui.QFont("맑은 고딕",20))
        #===============================================================================
        #clock_button 이라는 이름으로 버튼을 생성 [쓰레드가 잘 작동하는지 확인]
        # self.clock_button = QtWidgets.QPushButton(self.centralwidget)
        # self.clock_button.setGeometry(QtCore.QRect(200, 280, 75, 23))
        # self.clock_button.setObjectName("clock_button")
        #===================================================================
        #===================================================================

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SmartMirror"))
        # self.clock_button.setText(_translate("MainWindow", "PushButton"))
        # self.youtube_button.setText(_translate("MainWindow", "Youtube"))

    #-----------------------------------------------------------------------------------------
    # 이벤트
    # EVENT
    #-----------------------------------------------------------------------------------------

    #버튼을 누를시
    # def button(self,MainWindow):
    #     self.clock_button.clicked.connect(self.hello) #누를시 hello 함수랑 연결
    #     self.youtube_button.clicked.connect(self.Stop_video)

    #프린트 hello world 함수
    def hello(self,MainWindow):
        self.hello_world = self.hello_world + 1
        self.clock.setText("%d %s" %(self.hello_world, "hello world"))

    #시간을 알려주는 함수 메인 화면에 생성
    # now.(year,month,day,hour,minute,second)
    def set_time(self,MainWindow):
        AmOrPm = "AM"
        while True:
            now=datetime.datetime.now()
            hour=now.hour

            if(now.hour>=12):
                AmOrPm="PM"
                hour=now.hour%12

                if(now.hour==12):
                    hour=12

            else:
                AmOrPm="AM"

            self.date.setText("%sY %sM %sD"%(now.year,now.month,now.day))
            self.time.setText(AmOrPm+" %s : %s" %(hour,now.minute))
            sleep(1)

    #weather (아이콘 설정 및 기온 출력)
    def weather_icon(self,MainWindow):
        while True:
            reqForWeather = urllib.request.Request("http://api.openweathermap.org/data/2.5/weather?q=Cheonan&units=metric&appid=f611edc8235273d9f945d6229d31186e")
            weatherData = urllib.request.urlopen(reqForWeather).read()
            dataFile = open("./weatherData.json", mode="w", encoding='utf-8')
            data_str = str(data, "utf-8")
            print(data_str)

            #대구소프트웨어고등학교 위치
            lat = 35.663106 
            lng = 128.413759

            #서버 접속후 데이터를 받아옴
            forecast = forecastio.load_forecast(api_key, lat, lng)
            weather=forecast.currently()


            weather_cashe=weather.icon

            self.temperature.setText("[ %.1f ℃ ]" %(weather.temperature))
            
            if "day" in weather_cashe:
                if "partly-cloudy" in weather_cashe:
                    self.weather.setPixmap(QtGui.QPixmap("weather_icon\cloudy_day.png"))
                elif "cloudy" in weather_cashe:
                    self.weather.setPixmap(QtGui.QPixmap("weather_icon\clouds.png"))
                elif "clear" in weather_cashe:
                    self.weather.setPixmap(QtGui.QPixmap("weather_icon\sun.png"))

            elif "night" in weather_cashe:
                if "partly-cloudy" in weather_cashe:
                    self.weather.setPixmap(QtGui.QPixmap("weather_icon\cloudy_night.png"))
                elif "cloudy" in weather_cashe:
                    self.weather.setPixmap(QtGui.QPixmap("weather_icon\clouds.png"))
                elif "clear" in weather_cashe:
                    self.weather.setPixmap(QtGui.QPixmap("weather_icon\moon.png"))
            
            elif "cloudy" in weather_cashe:
                self.weather.setPixmap(QtGui.QPixmap("weather_icon\clouds.png"))

            elif "rain" in weather_cashe:
                self.weather.setPixmap(QtGui.QPixmap("weather_icon\drop.png"))

            elif "snow" in weather_cashe:
                self.weather.setPixmap(QtGui.QPixmap("weather_icon\snowflake.png"))

            sleep(300)

    def Video_to_frame(self, MainWindow):
        while True:
            url = "https://youtu.be/"

            api = yapi.YoutubeAPI('youtube_data_api_ver3_key')
            video_name="자막뉴스 "
            results = api.general_search(video_name, max_results=2)
            
            str_results=str(results)

            i=0
            TrueOrFalse=False
            video_id=""

            #print(str_results)
            
            while True:
                try :

                    if "'" in str_results[i]:
                        if "=" in str_results[i-1]:
                            if "d" in str_results[i-2]:
                                if "I" in str_results[i-3]:
                                    if "o" in str_results[i-4]:
                                        i=i+1
                                        TrueOrFalse=True
                                        break
                    i=i+1

                except IndexError as e:
                    print("error")
                    break

            while TrueOrFalse:
                if "'" in str_results[i]:
                    break
                else :
                    video_id=video_id+str_results[i]

                i=i+1

            url = url+video_id

            try :
                vPafy = pafy.new(url)
                self.video_name_label.setText(vPafy.title)
                video_length=vPafy.length/60

            except Exception as e :
                self.video_viewer_label.setText("Error")
                self.start=False
            print(video_length/60)

            play = vPafy.getbest(preftype="mp4")
                
            cap = cv2.VideoCapture(play.url)

            while self.start:
                self.ret, self.frame = cap.read()
                if self.ret:
                    self.rgbImage = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                    self.convertToQtFormat = QImage(self.rgbImage.data, self.rgbImage.shape[1], self.rgbImage.shape[0], QImage.Format_RGB888)
                       
                    self.pixmap = QPixmap(self.convertToQtFormat)
                    self.p = self.pixmap.scaled(400, 225, QtCore.Qt.IgnoreAspectRatio)

                    self.video_viewer_label.setPixmap(self.p)
                    self.video_viewer_label.update()

                    sleep(0.02) #Youtube 영상 1프레임당 0.02초

                else :
                    break
                    
                if self.start_or_stop:
                    break

            cap.release()
            cv2.destroyAllWindows()
                
    # def Stop_video(self,MainWindow) :
    #     if self.start_or_stop :
    #         self.start_or_stop=False
    #     else :
    #         self.start_or_stop=True

    #----------------------------------------------------------------------------------------------------
    #------------------------ 쓰레드 ---------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------

    #Set_time을 쓰레드로 사용
    def time_start(self,MainWindow):
        thread=threading.Thread(target=self.set_time,args=(self,))
        thread.daemon=True #프로그램 종료시 프로세스도 함께 종료 (백그라운드 재생 X)
        thread.start()

    #weather_icon을 쓰레드로 사용
    def weather_start(self,MainWindow):
        thread=threading.Thread(target=self.weather_icon,args=(self,))
        thread.daemon=True #프로그램 종료시 프로세스도 함께 종료 (백그라운드 재생 X)
        thread.start()

    #video_to_frame을 쓰레드로 사용
    def video_thread(self,MainWindow):
        thread=threading.Thread(target=self.Video_to_frame,args=(self,))
        thread.daemon=True #프로그램 종료시 프로세스도 함께 종료 (백그라운드 재생 X)
        thread.start()

#-------------메인---------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------

if __name__=="__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    ui = Ui_MainWindow()

    ui.setupUi(MainWindow)
    # ui.button(MainWindow)

    ui.time_start(MainWindow) #time thread
    ui.weather_start(MainWindow) #weather thread
    ui.video_thread(MainWindow) #video thread

    MainWindow.show()

    sys.exit(app.exec_())
                        