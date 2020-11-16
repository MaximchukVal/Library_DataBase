class modifyBookTypeWin(QWidget):
    def __init__(self, con):
        super().__init__()
        self.con = con

    def initUI(self, table):
        self.table = table
        self.setGeometry(760, 350, 400, 300)
        self.setFixedSize(self.size())
        self.setWindowTitle('Modify book type')
        self.setWindowIcon(QIcon(r'C:\Users\shmel\PycharmProjects\DataBase\lib.png'))

        l0 = QLabel('Type ID:', self)
        l0.move(30, 20)

        cur = self.con.cursor()
        cur.execute("select id from book_types")
        Items = []
        for row in cur:
            Items.append(str(row[0]))
        self.CBox = QComboBox(self)
        self.CBox.addItems(Items)
        self.CBox.currentTextChanged.connect(self.viewClient)
        self.CBox.move(190, 20)

        cur = self.con.cursor()
        cur.execute('select * from book_types')
        line = cur.fetchone()

        l1 = QLabel('New name:', self)
        l1.move(60, 100)

        self.nameEdit = QLineEdit(self)
        self.nameEdit.move(190, 70)
        self.nameEdit.setText(line[1])

        self.fineEdit = QLineEdit(self)
        self.fineEdit.move(190, 120)
        self.fineEdit.setText(str(line[3]))

        self.dayEdit = QLineEdit(self)
        self.dayEdit.move(190, 170)
        self.dayEdit.setText(str(line[4]))

        btnGo = QPushButton('Modify', self)
        btnGo.move(150, 260)
        btnGo.clicked.connect(self.btnGoClicked)

        self.show()

    def viewClient(self):
        cur = self.con.cursor()
        cur.execute(r"select * from book_types where id = " + self.CBox.currentText())
        line = cur.fetchone()
        self.nameEdit.setText(line[1])
        self.fineEdit.setText(str(line[3]))
        self.dayEdit.setText(str(line[4]))

    def btnGoClicked(self):
        parameters = [self.CBox.currentText(), self.nameEdit.text(), self.fineEdit.text(), self.dayEdit.text()]
        cur = self.con.cursor()
        try:
            cur.callproc('PROC_UPDATE_BOOK_TYPE', parameters)
        except:
            error_d = QMessageBox()
            error_d.setIcon(QMessageBox.Critical)
            error_d.setText("You are not allowed to modify this book type")
            error_d.setWindowTitle("Error!")
            error_d.exec_()
            return
        self.con.commit()

        cur = self.con.cursor()
        cur.execute('select count(*) from book_types')
        num_rows = cur.fetchone()[0]
        self.table.setRowCount(num_rows)
        self.table.setHorizontalHeaderLabels(['ID', 'Name', 'Count', 'Fine', 'Days'])
        cur.execute('select * from book_types order by id')
        l = cur.fetchall()
        ll = []
        for el in l:
            ll.append(list(el))
        for i in range(0, num_rows):
            for j in range(0, 5):
                self.table.setItem(i, j, QTableWidgetItem(str(ll[i][j])))
        self.table.resizeColumnsToContents()
        self.close()