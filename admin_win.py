import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QLabel
from PyQt5.QtGui import QFont
from multiprocessing import Process
import face_add as f
import encode_faces as train
import Main as M
import firebase

Lid={"1234":"R_No"}

class Admin_fun(QMainWindow):
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

        self.button = QPushButton("Add Student",self)
        self.button.move(200, 110)
        self.button.clicked.connect(self.on_add)

        self.button2 = QPushButton("Train", self)
        self.button2.move(200, 180)
        self.button2.clicked.connect(self.train)


        self.button1 = QPushButton("Exit",self)
        self.button1.move(200, 240)
        self.button1.clicked.connect(self.on_exit)
        self.show()

    def on_add(self):
        self.add = Add_Student()
        self.add.show()
        self.close()

    def train(self):
        p2 = Process(train.train())
        p2.start()
        p2.join()
        QMessageBox.about(self, "Training", "Trained Successful")


    def on_exit(self):
        self.main = M.App()
        self.main.show()
        self.close()


class Add_Student(QMainWindow):
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

        self.label = QLabel('Name :', self)
        self.label.move(100,40)

        self.Name = QLineEdit(self)
        self.Name.move(100, 80)
        self.Name.resize(280, 40)

        self.pass1 = QLabel('Roll No :', self)
        self.pass1.move(100, 130)

        self.R_No = QLineEdit(self)
        self.R_No.move(100, 170)
        self.R_No.resize(280, 40)

        self.button = QPushButton('Submit', self)
        self.button.move(200, 230)
        self.button.clicked.connect(self.on_click)

        self.show()

    def on_click(self):
        print(self.Name.text())
        print(type(self.label.text()))
        if len(self.Name.text()) != 0 :
            if len(self.R_No.text()) != 0:
                firebase.addstudent(name=self.Name, rollno=self.label.text())
                self.Train = Train_Student(self.Name.text(),self.R_No.text())
                self.Train.show()
                self.close()

class Train_Student(QMainWindow):
    def __init__(self,Name,R_No):
        super().__init__()
        self.name = Name
        self.rno = R_No
        self.title = 'Attendance Management System'
        self.left = 550
        self.top = 250
        self.width = 500
        self.height = 500
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.button = QPushButton('Take Photo', self)
        self.button.move(200, 180)
        self.button.clicked.connect(self.on_click_face_add)

        self.button = QPushButton('Home', self)
        self.button.move(200, 250)
        self.button.clicked.connect(self.on_click_Train)

    def on_click_face_add(self):
        print("add face")
        f.add(self.name)
    def on_click_Train(self):
        print("Home")
        self.mainwindow=Admin_fun()
        self.mainwindow.show()
        self.close()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Admin_fun()
    sys.exit(app.exec_())