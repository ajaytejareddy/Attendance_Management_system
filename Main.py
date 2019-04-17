import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton,QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import GUI_admin as admin
import GUI_Lecutrer as lect

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Attendance Management System'
        self.left = 550
        self.top = 250
        self.width = 500
        self.height = 500
        self.initUI()


    def initUI(self):
        self.setWindowIcon(QIcon("index.jpg"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        button1 = QPushButton('Admin', self)
        button1.setToolTip('Admin Login')
        button1.move(180, 150)
        button1.resize(120,35)
        button1.clicked.connect(self.on_click1)

        button2 = QPushButton('Lecturer', self)
        button2.setToolTip('Admin Login')
        button2.move(180, 220)
        button2.resize(120,35)
        button2.clicked.connect(self.on_click2)

        self.show()


    @pyqtSlot()
    def on_click1(self):
        print("Admin Login")
        self.cams=admin.Login_Admin()
        self.cams.show()
        self.close()

    def on_click2(self):
        print("Lecturer Login")
        self.cams = lect.Login_Lecturer()
        self.cams.show()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())