from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from PIL import ImageTk, Image
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import *
import os
import tool_name


Name = ""
ID1 = ""
URL = ""

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
        self.buttonOK = QtWidgets.QPushButton("NEXT", self)
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

        import vlc_scraper_1
        vlc_scraper_1.scrape_all_reviews(Name, ID1, URL)

if __name__ == "__main__":
    import sys
    # os.system("tool_name.py")
    app = QtWidgets.QApplication(sys.argv)
    myapp = PyQtApp()
    myapp.show()
    sys.exit(app.exec_())