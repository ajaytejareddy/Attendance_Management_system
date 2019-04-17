import sys

from PyQt5 import QtGui,QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QLabel
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import pyqtSlot
import admin_win as aw


login={"Root":"password"}

class Login_Admin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Attendance Management System'
        self.left = 550
        self.top = 250
        self.width = 500
        self.height = 500
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.label = QLabel('ADMIN ID :', self)
        self.label.move(100,40)

        self.textbox = QLineEdit(self)
        self.textbox.move(100, 80)
        self.textbox.resize(280, 40)

        self.pass1 = QLabel('PASSWORD :', self)
        self.pass1.move(100, 130)

        self.password = QLineEdit(self)
        self.password.move(100, 170)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.resize(280, 40)

        self.button = QPushButton('Login', self)
        self.button.move(200, 230)
        self.button.clicked.connect(self.on_login)

        self.show()

    def on_login(self):
        if self.textbox.text() in login :
            if self.password.text() == login[self.textbox.text()]:
                self.cams = aw.Admin_fun()
                self.cams.show()
                self.close()

