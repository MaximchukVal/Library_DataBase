class modifyBooksWin(QWidget):
    def __init__(self, con):
        super().__init__()
        self.con = con

    def initUI(self, table):
        self.table = table
        self.setGeometry(760, 350, 400, 300)
        self.setFixedSize(self.size())
        self.setWindowTitle('Modify books')
        self.setWindowIcon(QIcon(r'C:\Users\shmel\PycharmProjects\DataBase\lib.png'))

        label = QLabel('Book ID:', self)
        label.move(QPoint(30, 20))

        cur = self.con.cursor()
        cur.execute("select id from books")
        items = []
        for row in cur:
            items.append(str(row[0]))
        self.CBox = QComboBox(self)
        self.CBox.addItems(items)
        self.CBox.currentTextChanged.connect(self.viewClient)
        self.CBox.move(QPoint(190, 20))

        cur = self.con.cursor()
        cur.execute("select * from books")
        line = cur.fetchone()

        l1 = QLabel('New book name:', self)
        l1.move(30, 70)
        self.bookNameEdit = QLineEdit(self)
        self.bookNameEdit.move(190, 70)
        self.bookNameEdit.setText(line[1])

        l2 = QLabel('New count:', self)
        l2.move(30, 120)

        self.countEdit = QLineEdit(self)
        self.countEdit.setValidator(QIntValidator())
        self.countEdit.move(190, 120)
        self.countEdit.setText(str(line[2]))

        l3 = QLabel('New type:', self)
        l3.move(30, 170)

        cur = self.con.cursor()
        cur.execute("select id, name from book_types")
        items = []
        self.types = dict()
        for row in cur:
            self.types[row[1]] = row[0]
            items.append(row[1])
        self.CBox_2 = QComboBox(self)
        self.CBox_2.addItems(items)
        self.CBox_2.move(QPoint(190, 170))

        btnGo = QPushButton('Modify', self)
        btnGo.move(150, 260)
        btnGo.clicked.connect(self.btnGoClicked)

        self.show()

    def viewClient(self):
        cur = self.con.cursor()
        cur.execute(r"select books.name, books.cnt, book_types.name from books "
                    r"inner join book_types on books.type_id = book_types.id and books.id = " + self.CBox.currentText())
        line = cur.fetchone()
        self.bookNameEdit.setText(line[0])
        self.countEdit.setText(str(line[1]))
        index = self.CBox_2.findText(line[2])
        if index >= 0:
            self.CBox_2.setCurrentIndex(index)

    def btnGoClicked(self):
        parameters = [self.CBox.currentText(), self.bookNameEdit.text(), self.countEdit.text(),
                      str(self.types[self.CBox_2.currentText()])]
        cur = self.con.cursor()
        if (self.bookNameEdit.text() == '' or self.countEdit.text() == ''):
            error_f = QMessageBox()
            error_f.setIcon(QMessageBox.Critical)
            error_f.setText("Please fill all fields!")
            error_f.setWindowTitle('Error!')
            error_f.exec()
            return
        try:
            cur.callproc('PROC_UPDATE_BOOK', parameters)
        except:
            error_d = QMessageBox()
            error_d.setIcon(QMessageBox.Critical)
            error_d.setText("You are not allowed to modify this book")
            error_d.setWindowTitle("Error!")
            error_d.exec_()
            return
        self.con.commit()

        cur = self.con.cursor()
        cur.execute('select count(*) from books')
        num_rows = cur.fetchone()[0]
        self.table.setRowCount(num_rows)
        self.table.setHorizontalHeaderLabels(['ID', 'Name', 'Count', 'Type'])
        cur.execute('select books.id, books.name, books.cnt, book_types.name from books '
                    'inner join book_types on books.type_id = book_types.id '
                    'order by books.id')
        l = cur.fetchall()
        ll = []
        for el in l:
            ll.append(list(el))
        for i in range(0, num_rows):
            for j in range(0, 4):
                self.table.setItem(i, j, QTableWidgetItem(str(ll[i][j])))
        self.close()