class addClientWin(QWidget):
    def __init__(self, con):
        super().__init__()
        self.con = con

    def initUI(self, table):
        self.table = table
        self.setGeometry(760, 350, 400, 300)
        self.setFixedSize(self.size())
        self.setWindowTitle('New client')
        self.setWindowIcon(QIcon(r'C:\Users\shmel\PycharmProjects\DataBase\lib.png'))

        l1 = QLabel('Client:   Last name:', self)
        l1.move(30, 40)
        self.FNameEdit = QLineEdit(self)
        self.FNameEdit.move(190, 40)

        l2 = QLabel('            First name:', self)
        l2.move(30, 80)
        self.INameEdit = QLineEdit(self)
        self.INameEdit.move(190, 80)

        l3 = QLabel('            Father name:', self)
        l3.move(30, 120)
        self.ONameEdit = QLineEdit(self)
        self.ONameEdit.move(190, 120)

        l4 = QLabel('Passport:   Seria:', self)
        l4.move(30, 160)
        self.seriaEdit = QLineEdit(self)
        re = QRegExp(r'[0-9]{4}')
        valid_1 = QRegExpValidator(re, self.seriaEdit)
        self.seriaEdit.setValidator(valid_1)
        self.seriaEdit.move(190, 160)

        l5 = QLabel('                 Number:', self)
        l5.move(30, 200)
        self.numEdit = QLineEdit(self)
        rule = QRegExp(r'[0-9]{6}')
        valid_2 = QRegExpValidator(rule, self.numEdit)
        self.numEdit.setValidator(valid_2)
        self.numEdit.move(190, 200)

        btnGo = QPushButton('Add', self)
        btnGo.move(150, 260)
        btnGo.clicked.connect(self.btnGoClicked)

        self.show()

    def btnGoClicked(self):
        parameters = [self.FNameEdit.text(), self.INameEdit.text(), self.ONameEdit.text(),
                      self.seriaEdit.text(), self.numEdit.text()]
        cur = self.con.cursor()
        if (self.FNameEdit.text() == '' or self.INameEdit.text() == '' or self.ONameEdit.text() == ''
                or self.seriaEdit.text() == '' or self.numEdit.text() == ''):
            error_f = QMessageBox()
            error_f.setIcon(QMessageBox.Critical)
            error_f.setText("Please fill all fields!")
            error_f.setWindowTitle('Error!')
            error_f.exec()
            return
        try:
            cur.callproc('PROC_ADD_NEW_CLIENT', parameters)
        except:
            error_d = QMessageBox()
            error_d.setIcon(QMessageBox.Critical)
            error_d.setText("You are not allowed to add this client")
            error_d.setWindowTitle("Error!")
            error_d.exec_()
            return
        self.con.commit()

        cur = self.con.cursor()
        cur.execute('select count(*) from clients')
        num_row = cur.fetchone()[0]
        self.table.setRowCount(num_row)
        self.table.setHorizontalHeaderLabels(
            ['ID', 'Family Name', 'Name', 'Father Name', 'Passport_seria', 'Passport_num'])
        cur.execute("select id, last_name, first_name, pather_name, passport_seria, passport_num from clients "
                    "order by id")
        l = cur.fetchall()
        ll = []
        for el in l:
            ll.append(list(el))
        for i in range(0, num_row):
            for j in range(0, 6):
                self.table.setItem(i, j, QTableWidgetItem(str(ll[i][j])))
        self.table.resizeColumnsToContents()
        self.close()