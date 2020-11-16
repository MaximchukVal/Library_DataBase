class JournalWindow(QWidget):
    def __init__(self, con):
        super().__init__()
        self.con = con
        self.borrowBook = BorrowBookWindow(self.con)
        self.returnBook = ReturnBookWindow(self.con)
        self.initUI()

    def initUI(self):
        self.setGeometry(510, 200, 800, 600)
        self.setFixedSize(self.size())
        self.setWindowTitle('Library Journal')
        self.setWindowIcon(QIcon(r'C:\Users\shmel\PycharmProjects\DataBase\lib.png'))

        self.table = QTableWidget(self)
        self.table.setMaximumSize(QSize(620, 550))
        self.table.setColumnCount(6)

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

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        scroll = QScrollArea()
        scroll.setWidget(self.table)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
        self.setLayout(layout)

        clientBtn = QPushButton('Clients', self)
        clientBtn.resize(QSize(120, 40))
        clientBtn.move(650, 80)
        clientBtn.clicked.connect(self.ClientButtonClicked)

        bookBtn = QPushButton('Books', self)
        bookBtn.setToolTip('Browse all the books')
        bookBtn.resize(QSize(120, 40))
        bookBtn.move(650, 130)
        bookBtn.clicked.connect(self.BookButtonClicked)

        booktypesBtn = QPushButton('Book types', self)
        booktypesBtn.setToolTip('Browse all the book types')
        booktypesBtn.resize(QSize(120, 40))
        booktypesBtn.move(650, 180)
        booktypesBtn.clicked.connect(self.BookTypeButtonClicked)

        newborBtn = QPushButton('New borrowed book', self)
        newborBtn.setToolTip('Issue the book to client')
        newborBtn.resize(QSize(120, 40))
        newborBtn.move(650, 230)
        newborBtn.action = 'Issue'
        newborBtn.clicked.connect(self.BorrowButtonClicked)

        newretBtn = QPushButton('New returned book', self)
        newretBtn.setToolTip('Refresh all tables')
        newretBtn.resize(QSize(120, 40))
        newretBtn.move(650, 280)
        newretBtn.clicked.connect(self.ReturnedButtonClicked)

        statBtn = QPushButton('Procedures', self)
        statBtn.setToolTip('Show procedures')
        statBtn.resize(QSize(120, 40))
        statBtn.move(650, 330)
        #statBtn.clicked.connect(self.ProcButtonClicked)

        self.show()

    def ClientButtonClicked(self):
        self.clientWindow = ClientWindow(self.con)
        self.close()

    def BookButtonClicked(self):
        self.bookWindow = BooksWindow(self.con)
        self.close()

    def BookTypeButtonClicked(self):
        self.booktypeWindow = BookTypeWindow(self.con)
        self.close()

    def BorrowButtonClicked(self):
        self.borrowBook.initUI(self.table)

    def ReturnedButtonClicked(self):
        self.returnBook.initUI(self.table)