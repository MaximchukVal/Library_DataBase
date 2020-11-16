class BorrowBookWindow(QWidget):
    def __init__(self, con):
        super().__init__()
        self.con = con

    def initUI(self, table):
        self.table = table
        self.setGeometry(760, 350, 400, 300)
        self.setFixedSize(self.size())
        self.setWindowTitle('New borrow book')
        self.setWindowIcon(QIcon(r'C:\Users\shmel\PycharmProjects\DataBase\lib.png'))


        l1 = QLabel('Book: ', self)
        l1.move(QPoint(30, 70))
        cur = self.con.cursor()
        cur.execute("select id, name from books")
        items = []
        self.types_1 = dict()
        for row in cur:
            self.types_1[row[1]] = row[0]
            items.append(row[1])
        self.CBox_1 = QComboBox(self)
        self.CBox_1.addItems(items)
        self.CBox_1.move(QPoint(190, 70))

        l2 = QLabel('Client: ', self)
        l2.move(QPoint(30, 120))
        cur = self.con.cursor()
        cur.execute("select id, concat(first_name, concat(' ',last_name)) from clients")
        items = []
        self.types_2 = dict()
        for row in cur:
            self.types_2[row[1]] = row[0]
            items.append(row[1])
        self.CBox_2 = QComboBox(self)
        self.CBox_2.addItems(items)
        self.CBox_2.move(QPoint(190, 120))

        l3 = QLabel('Date: ', self)
        l3.move(30, 170)
        self.dateEdit = QLineEdit(self)
        re = QRegExp(r'[0-9]{4}/{1}[0-9]{2}/{1}[0-9]{2}')
        myValidator = QRegExpValidator(re, self.dateEdit)
        self.dateEdit.setValidator(myValidator)
        self.dateEdit.move(190, 170)

        btnGo = QPushButton('Submit', self)
        btnGo.move(QPoint(150, 260))
        btnGo.clicked.connect(self.btnGoClicked)

        self.show()

    def btnGoClicked(self):
        parameters = [self.types_1[self.CBox_1.currentText()], self.types_2[self.CBox_2.currentText()], self.dateEdit.text()]
        print(parameters)
        cur = self.con.cursor()
        try:
            cur.callproc('PROC_ADD_NEW_BORROWED_BOOK', parameters)
        except:
            error_d = QMessageBox()
            error_d.setIcon(QMessageBox.Critical)
            error_d.setText("You are not allowed to get this book")
            error_d.setWindowTitle("Error!")
            error_d.exec_()
            return
        self.con.commit()

        cur = self.con.cursor()
        cur.execute('select count(*) from journal')
        num_rows = cur.fetchone()[0]
        self.table.setRowCount(num_rows)
        self.table.setHorizontalHeaderLabels(['ID', 'Book', 'Client', 'Date begin', 'Date end', 'Date return'])
        cur.execute("select journal.id, books.name, concat(first_name, concat(' ',last_name)), "
                    "date_beg, date_end, date_ret from journal "
                    "inner join books on journal.book_id = books.id "
                    "inner join clients on journal.client_id = clients.id "
                    "order by journal.id")
        l = cur.fetchall()
        ll = []
        for el in l:
            ll.append(list(el))
        for i in range(0, num_rows):
            for j in range(0, 6):
                string = str(ll[i][j])
                if j > 2:
                    string = string[:10]
                self.table.setItem(i, j, QTableWidgetItem(string))

        self.table.resizeColumnsToContents()

        self.close()