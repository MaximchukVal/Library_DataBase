import journal_win

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QMessageBox
from PyQt5.QtGui import *


class EnterWindow(QWidget):
    def __init__(self, con):
        super().__init__()
        self.con = con

        self.setGeometry(600, 200, 300, 160)
        self.setFixedSize(self.size())
        self.setWindowTitle('Logging in')
        self.setWindowIcon(QIcon(r'C:\Users\shmel\PycharmProjects\DataBase\lib.png'))

        self.l1 = QLabel('Login:', self)
        self.l1.move(20, 30)
        self.l1 = QLabel('Password:', self)
        self.l1.move(20, 60)

        self.lgnEdit = QLineEdit(self)
        self.lgnEdit.move(100, 30)
        self.pswEdit = QLineEdit(self)
        self.pswEdit.move(100, 60)
        self.pswEdit.setEchoMode(QLineEdit.Password)

        self.btn = QPushButton('Sign in', self)
        self.btn.move(100, 100)
        self.btn.clicked.connect(self.enterClicked)

        self.show()

    def enterClicked(self):
        login = self.lgnEdit.text()
        password = self.pswEdit.text()
        if len(login) == 0 or len(password) == 0:
            error_d = QMessageBox()
            error_d.setIcon(QMessageBox.Critical)
            error_d.setText("Enter login and password!")
            error_d.setWindowTitle("Error!")
            error_d.exec_()
            return
        else:
            try:
                con = self.con.getDBconnection(login, password)
            except:
                error_d = QMessageBox()
                error_d.setIcon(QMessageBox.Critical)
                error_d.setText("Invalid login and password!")
                error_d.setWindowTitle("Error!")
                error_d.exec_()
                return
            print("Connection is successful")
            self.startWindow = journal_win.Journal_win(self.con)
            self.close()
