class addBookTypeWin(QWidget):
    def __init__(self, con):
        super().__init__()
        self.con = con

    def initUI(self, table):
        self.table = table
        self.setGeometry(760, 350, 400, 300)
        self.setFixedSize(self.size())
        self.setWindowTitle('New borrowed book')
        self.setWindowIcon(QIcon(r'C:\Users\shmel\PycharmProjects\DataBase\lib.png'))

        l1 = QLabel('Name:', self)
        l1.move(30, 70)

        self.nameEdit = QLineEdit(self)
        self.nameEdit.move(190, 70)

        l2 = QLabel('Fine:', self)
        l2.move(30, 120)

        self.fineEdit = QLineEdit(self)
        self.fineEdit.setValidator(QIntValidator())
        self.fineEdit.move(190, 120)

        l3 = QLabel('Days:', self)
        l3.move(30, 170)

        self.daysEdit = QLineEdit(self)
        self.daysEdit.setValidator(QIntValidator())
        self.daysEdit.move(190, 170)

        btnGo = QPushButton('Add', self)
        btnGo.move(QPoint(150, 260))
        btnGo.clicked.connect(self.btnGoClicked)

        self.show()

    def btnGoClicked(self):
        parameters = [self.nameEdit.text(), self.fineEdit.text(), self.daysEdit.text()]
        cur = self.con.cursor()
        try:
            cur.callproc('PROC_ADD_NEW_BOOK_TYPE', parameters)
        except:
            error_d = QMessageBox()
            error_d.setIcon(QMessageBox.Critical)
            error_d.setText("You are not allowed to add this book type")
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