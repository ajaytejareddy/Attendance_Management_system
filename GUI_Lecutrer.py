import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QLabel
from PyQt5.QtGui import QFont
import recognize_faces_video as R
import firebase as fb
import view_report as report_generate
import Main as m

Lid={"1234":"password"}

class Login_Lecturer(QMainWindow):
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

        self.label = QLabel('LECTURER ID :', self)
        self.label.move(100,40)

        self.textbox = QLineEdit(self)
        self.textbox.move(100, 80)
        self.textbox.resize(280, 40)

        self.pass1 = QLabel('PASSWORD :', self)
        self.pass1.move(100, 130)

        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.Password)
        self.password.move(100, 170)
        self.password.resize(280, 40)

        self.button = QPushButton('Login', self)
        self.button.move(200, 230)
        self.button.clicked.connect(self.on_click)

        self.show()

    def on_click(self):
        print(self.textbox.text())
        print(type(self.label.text()))
        if self.textbox.text() in Lid :
            if self.password.text() == Lid[self.textbox.text()]:
                self.cams = L_Window(self.textbox.text())
                self.cams.show()
                self.close()


class L_Window(QMainWindow):
    def __init__(self,ID):
        super().__init__()
        self.id=ID
        self.title = 'Attendance Management System'
        self.left = 550
        self.top = 250
        self.width = 500
        self.height = 500
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.label = QLabel(self.id, self)
        self.label.setFont(QFont("Times", 12,QFont.Bold))


        self.button1 = QPushButton("start class", self)
        self.button1.setToolTip("test")
        self.button1.move(200, 160)
        self.button1.resize(125, 35)
        self.button1.clicked.connect(self.on_click_start)

        self.button2 = QPushButton("stop", self)
        self.button2.setToolTip("test")
        self.button2.move(200, 220)
        self.button2.resize(125, 35)
        self.button2.clicked.connect(self.on_click_stop)

        self.button3 = QPushButton("View Report", self)
        self.button3.setToolTip("test")
        self.button3.move(200, 280)
        self.button3.resize(125, 35)
        self.button3.clicked.connect(self.on_click_veiw)

        self.button2 = QPushButton("Exit", self)
        self.button2.setToolTip("Exit to login window")
        self.button2.move(200, 340)
        self.button2.resize(125, 35)
        self.button2.clicked.connect(self.on_Exit)

        self.show()

    def on_click_start(self):
        #print("start")
        R.start()

    def on_click_stop(self):
        print("stop")
        att,held = R.stop()
        #print(held)
        #print(att)
        fb.Firebase_attendance(att)
        fb.Total_held(held)

    def on_click_veiw(self):
        print("view Report")
        report_generate.main()

    def on_Exit(self):
        self.main = m.App()
        self.main.show()
        self.close()
