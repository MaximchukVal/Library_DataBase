class modifyClientWin(QWidget):
    def __init__(self, con):
        super().__init__()
        self.con = con
        self.CBox = QComboBox(self)

    def initUI(self, table):
        self.table = table
        self.setGeometry(760, 350, 400, 300)
        self.setFixedSize(self.size())
        self.setWindowTitle('Modify client')
        self.setWindowIcon(QIcon(r'C:\Users\shmel\PycharmProjects\DataBase\lib.png'))

        label = QLabel('Client ID:', self)
        label.move(QPoint(30, 20))

        cur = self.con.cursor()
        cur.execute("select id from clients")
        items = []
        for row in cur:
            items.append(str(row[0]))
        self.CBox.addItems(items)
        self.CBox.move(QPoint(190, 20))
        self.CBox.currentTextChanged.connect(self.viewClient)

        cur = self.con.cursor()
        cur.execute(r"select * from clients where id = " + self.CBox.currentText())
        line = cur.fetchone()

        l1 = QLabel('New family name:', self)
        l1.move(30, 60)
        self.FNameEdit = QLineEdit(self)
        self.FNameEdit.move(190, 60)
        self.FNameEdit.setText(line[2])

        l2 = QLabel('New name:', self)
        l2.move(30, 100)
        self.INameEdit = QLineEdit(self)
        self.INameEdit.move(190, 100)
        self.INameEdit.setText(line[1])


        l3 = QLabel('New father name:', self)
        l3.move(30, 140)
        self.ONameEdit = QLineEdit(self)
        self.ONameEdit.move(190, 140)
        self.ONameEdit.setText(line[3])


        l4 = QLabel('New passport seria:', self)
        l4.move(30, 180)
        self.seriaEdit = QLineEdit(self)
        rule = QRegExp(r'[0-9]{4}')
        valid_1 = QRegExpValidator(rule, self.seriaEdit)
        self.seriaEdit.setValidator(valid_1)
        self.seriaEdit.move(190, 180)
        self.seriaEdit.setText(line[4])


        l5 = QLabel('New passport number:', self)
        l5.move(30, 220)
        self.numEdit = QLineEdit(self)
        rule = QRegExp(r'[0-9]{6}')
        valid_2 = QRegExpValidator(rule, self.numEdit)
        self.numEdit.setValidator(valid_2)
        self.numEdit.move(190, 220)
        self.numEdit.setText(line[5])


        btnGo = QPushButton('Modify', self)
        btnGo.move(150, 260)
        btnGo.clicked.connect(self.btnGoClicked)

        self.show()

    def viewClient(self):
        cur = self.con.cursor()
        cur.execute(r"select * from clients where id = " + self.CBox.currentText())
        line = cur.fetchone()
        self.FNameEdit.setText(line[2])
        self.INameEdit.setText(line[1])
        self.ONameEdit.setText(line[3])
        self.seriaEdit.setText(line[4])
        self.numEdit.setText(line[5])

    def btnGoClicked(self):
        parameters = [self.CBox.currentText(), self.FNameEdit.text(), self.INameEdit.text(), self.ONameEdit.text(),
                      self.seriaEdit.text(), self.numEdit.text()]
        cur = self.con.cursor()
        if (self.FNameEdit.text() == '' or self.INameEdit.text() == '' or self.ONameEdit.text() == ''
                or self.seriaEdit.text() == '' or self.numEdit.text()):
            error_f = QMessageBox()
            error_f.setIcon(QMessageBox.Critical)
            error_f.setText("Please fill all fields!")
            error_f.setWindowTitle('Error!')
            error_f.exec()
            return
        try:
            cur.callproc('PROC_UPDATE_CLIENT', parameters)
        except:
            error_d = QMessageBox()
            error_d.setIcon(QMessageBox.Critical)
            error_d.setText("You are not allowed to modify this client")
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