class delBooksWin(QWidget):
    def __init__(self, con):
        super().__init__()
        self.con = con

    def initUI(self, table):
        self.table = table
        self.setGeometry(760, 350, 300, 200)
        self.setFixedSize(self.size())
        self.setWindowTitle('Delete book')
        self.setWindowIcon(QIcon(r'C:\Users\shmel\PycharmProjects\DataBase\lib.png'))

        l1 = QLabel('Book ID:', self)
        l1.move(50, 62)

        cur = self.con.cursor()
        cur.execute("select id from books")
        items = []
        for row in cur:
            items.append(str(row[0]))
        self.CBox = QComboBox(self)
        self.CBox.addItems(items)
        self.CBox.move(170, 60)

        btnGo = QPushButton('Delete', self)
        btnGo.move(QPoint(80, 130))
        btnGo.clicked.connect(self.btnGoClicked)

        self.show()

    def btnGoClicked(self):
        cur = self.con.cursor()
        parameters = [self.CBox.currentText()]
        try:
            cur.callproc('PROC_DELETE_BOOK', parameters)
        except:
            error_d = QMessageBox()
            error_d.setIcon(QMessageBox.Critical)
            error_d.setText("You are not allowed to delete this book")
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