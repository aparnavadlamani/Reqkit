from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from PIL import ImageTk, Image
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import *
import os
import tool_name
import time
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QToolTip, QMessageBox, QLabel

import vlc_scraper_1
import data_processing
import Supervised_model
import push_in_git
import python_to_mysql
import dbtocsv
#import SRS

Name = ""
ID1 = ""
URL = ""

class TaskThreadCollectData(QtCore.QThread):
    taskFinished = QtCore.pyqtSignal()
    def run(self):
        time.sleep(5)
        print("In thread: ", Name,ID1, URL)
        dbtocsv.export(Name+'db',Name, ID1, URL)
        self.taskFinished.emit()

class TaskThreadProcessData(QtCore.QThread):
    taskFinished = QtCore.pyqtSignal()
    def run(self):
        time.sleep(5)
        data_processing.process_data()
        self.taskFinished.emit()

class TaskThreadTrainAndPredict(QtCore.QThread):
    taskFinished = QtCore.pyqtSignal()
    def run(self):
        time.sleep(5)
        Supervised_model.classification_model()
        self.taskFinished.emit()

class TaskThreadPushGit(QtCore.QThread):
    taskFinished = QtCore.pyqtSignal()
    def run(self):
        # time.sleep(2)
        push_in_git.post_issue_git()
        SRS.srs_generation()
        self.taskFinished.emit()

class Window3(QMainWindow):            
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Progress Backend")
        self.setGeometry(100, 50, 700, 500)
        self.setStyleSheet("background-color: white;")

        self.label1 = QLabel(self)
        self.label1.setPixmap(QPixmap('reqkit_logo.png.svg'))
        self.label1.setGeometry(250,15, 200, 200)

        self.label2 = QLabel("Generates Requirements and pushes automatically in git",self)
        self.label2.setGeometry(180,250, 400, 20)

        self.progressBar = QProgressBar(self)
        self.progressBar.setGeometry(130, 250+35, 450, 20)
        self.progressBar.setRange(0,1)
        self.myTask = TaskThreadPushGit()
        self.onStart()

        self.buttonOK = QtWidgets.QPushButton("STOP PROCESS", self)
        self.buttonOK.resize(100,32)
        self.buttonOK.clicked.connect(self.clickMethod1)
        self.buttonOK.move(275,350)

    def onStart(self): 
        self.progressBar.setRange(0,0)
        self.myTask.start()
        self.myTask.taskFinished.connect(self.onFinished)

    def onFinished(self):
        self.progressBar.setRange(0,1)

    def clickMethod1(self):
        print('Clicked Pyqt button. This force stops the process')
        self.hide()
        exit(0)

class Window2(QMainWindow):            
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Progress Backend")
        self.setGeometry(100, 50, 700, 700)
        self.setStyleSheet("background-color: white;")

        self.label1 = QLabel(self)
        self.label1.setPixmap(QPixmap('reqkit_logo.png.svg'))
        self.label1.setGeometry(250,15, 200, 200)
        self.y = 225 
        self.label2 = QLabel("Collecting/Scraping Data",self)
        self.label2.setGeometry(285,self.y,400,15)

        self.label3 = QLabel("(Wait for Progress Bar to turn white)",self)
        self.label3.setGeometry(250, self.y+15, 500, 25)

        self.progressBar = QProgressBar(self)
        self.progressBar.setGeometry(130, self.y+45, 450, 20)
        self.progressBar.setRange(0,1)
        self.myTask = TaskThreadCollectData()
        self.onStart()

        self.label4 = QLabel(self)
        self.label4.setGeometry(237,self.y+70,400, 20)

        self.label5 = QLabel("Processing Data",self)
        self.label5.setGeometry(285,self.y+105,400,15)

        self.label6 = QLabel("(Wait for Progress Bar to turn white)",self)
        self.label6.setGeometry(250, self.y+120, 500, 25)

        self.progressBar1 = QProgressBar(self)
        self.progressBar1.setGeometry(130, self.y+140, 450, 20)
        self.progressBar1.setRange(0,1)

        self.label7 = QLabel(self)
        self.label7.setGeometry(237,self.y+175,400, 20)

        self.y = self.y+175+35

        self.label8 = QLabel("Training model and Predicting Output",self)
        self.label8.setGeometry(250,self.y,400,15)

        self.label9 = QLabel("(Wait for Progress Bar to turn white)",self)
        self.label9.setGeometry(250, self.y+15, 500, 25)

        self.progressBar2 = QProgressBar(self)
        self.progressBar2.setGeometry(130, self.y+45, 450, 20)
        self.progressBar2.setRange(0,1)
        

        self.label10 = QLabel(self)
        self.label10.setGeometry(217,self.y+70,400, 20)

        self.buttonOK = QtWidgets.QPushButton("Generate Requirements", self)
        self.buttonOK.resize(400,32)
        self.buttonOK.clicked.connect(self.clickMethod1)
        self.buttonOK.move(150,550)

    def onStart(self): 
        self.progressBar.setRange(0,0)
        self.myTask.start()
        self.myTask.taskFinished.connect(self.onFinished)

    def onStart1(self): 
        self.myTask1 = TaskThreadProcessData()
        self.progressBar1.setRange(0,0)
        self.myTask1.start()
        self.myTask1.taskFinished.connect(self.onFinished1)

    def onStart2(self):
        self.myTask2 = TaskThreadTrainAndPredict()
        self.progressBar2.setRange(0,0)
        self.myTask2.start()
        self.myTask2.taskFinished.connect(self.onFinished2)

    def clickMethod1(self):
        print('Clicked Pyqt button.')
        self.hide()
        self.w = Window3()
        self.w.show()

    def onFinished(self):
        self.progressBar.setRange(0,1)
        self.label4.setText("Reviews extracted! Output: test1.csv")
        self.onStart1()

    def onFinished1(self):
        self.progressBar1.setRange(0,1)
        self.label7.setText("Reviews Processed! Output: Processed1.csv")
        self.onStart2()

    def onFinished2(self):
        self.progressBar2.setRange(0,1)
        self.label10.setText("Model Trained! Labels Predicted! Output: dataset_output.csv")

class PyQtApp(QtWidgets.QWidget):
   
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setWindowTitle("REQKIT")
        self.setWindowIcon(QtGui.QIcon("/reqkit_logo.png"))
        self.setGeometry(100, 100, 700, 700)
        self.label = QLabel(self)
        self.label.setPixmap(QPixmap('reqkit_logo.png.svg'))
        self.label.setGeometry(250,50, 200, 200)
        self.setStyleSheet("background-color: white;")
        self.createFormGroupBox()
        self.buttonOK = QtWidgets.QPushButton("Check database and get reviews", self)
        self.buttonOK.resize(100,32)
        self.buttonOK.clicked.connect(self.clickMethod)
        # layout.addWidget(self.buttonOK, 1, 1)
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.label, 0, Qt.AlignHCenter)
        mainLayout.addWidget(self.formGroupBox, 1, Qt.AlignTop)
        mainLayout.addWidget(self.buttonOK,2,Qt.AlignTop)
        # self.Name = ""
        # self.ID1 = ""
        # self.URL = ""
        self.setLayout(mainLayout)

    def new_window(self):
        self.w = Window2()
        self.w.show()

    def createFormGroupBox(self):
        self.formGroupBox = QGroupBox("Details of the Application: (Ref: Google Play)")
        layout = QFormLayout()
        self.name = QLineEdit()
        self.id = QLineEdit()
        self.git_url = QLineEdit()
        layout.addRow(QLabel("App Name:"), self.name)
        layout.addRow(QLabel("App ID:"), self.id)
        layout.addRow(QLabel("Github URL:"), self.git_url)
        self.formGroupBox.setLayout(layout)

    def clickMethod(self):
        print('Clicked Pyqt button.')
        global Name, ID1, URL 
        Name = self.name.text()
        ID1 = self.id.text()
        URL = self.git_url.text()
        self.print_details()

    def print_details(self):

        print("App Name: ", Name)
        print("App ID: ", ID1)
        print("Github URL: ", URL)
        self.hide()
        self.new_window()

        # import vlc_scraper_1
        # vlc_scraper_1.scrape_all_reviews(Name, ID1, URL)


if __name__ == "__main__":
    import sys
    # os.system("tool_name.py")
    app = QtWidgets.QApplication(sys.argv)
    myapp = PyQtApp()
    myapp.show()

    sys.exit(app.exec_())
