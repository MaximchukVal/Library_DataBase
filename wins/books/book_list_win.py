class BooksWindow(QWidget):
    def __init__(self, con):
        super().__init__()
        self.con = con
        self.addWindow = addBooksWin(self.con)
        self.modWindow = modifyBooksWin(self.con)
        self.delWindow = delBooksWin(self.con)
        self.initUI()

    def initUI(self):
        self.setGeometry(510, 200, 800, 600)
        self.setFixedSize(self.size())
        self.setWindowTitle('Books')
        self.setWindowIcon(QIcon(r'C:\Users\shmel\PycharmProjects\DataBase\lib.png'))

        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setMaximumSize(QSize(620, 550))

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

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        scroll = QScrollArea()
        scroll.setWidget(self.table)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
        self.setLayout(layout)

        btnAdd = QPushButton('Add new book', self)
        btnAdd.resize(QSize(120, 40))
        btnAdd.move(650, 80)
        btnAdd.clicked.connect(self.addNewBook)

        btnMofidy = QPushButton('Modify table', self)
        btnMofidy.resize(QSize(120, 40))
        btnMofidy.move(650, 130)
        btnMofidy.clicked.connect(self.modifyBook)

        btnDelete = QPushButton('Delete book', self)
        btnDelete.resize(QSize(120, 40))
        btnDelete.move(650, 180)
        btnDelete.clicked.connect(self.deleteBook)

        btnBack = QPushButton('Back', self)
        btnBack.resize(QSize(120, 40))
        btnBack.move(650, 450)
        btnBack.clicked.connect(self.backButton)

        self.show()

    def addNewBook(self):
       self.addWindow.initUI(self.table)

    def modifyBook(self):
        self.modWindow.initUI(self.table)

    def deleteBook(self):
        self.delWindow.initUI(self.table)

    def backButton(self):
        self.journalWindow = Journal_win(self.con)
        self.close()