from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Journal_win(QWidget):
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

class ClientWindow(QWidget):
    def __init__(self, con):
        super().__init__()
        self.con = con
        self.addWindow = addClientWin(self.con)
        self.modWindow = modifyClientWin(self.con)
        self.delWindow = delClientWin(self.con)
        self.initUI()

    def initUI(self):
        self.setGeometry(510, 200, 800, 600)
        self.setFixedSize(self.size())
        self.setWindowTitle('Clients')
        self.setWindowIcon(QIcon(r'C:\Users\shmel\PycharmProjects\DataBase\lib.png'))

        self.table = QTableWidget(self)
        self.table.setColumnCount(6)
        self.table.setMaximumSize(QSize(620, 550))

        cur = self.con.cursor()
        cur.execute('select count(*) from clients')
        num_row = cur.fetchone()[0]
        self.table.setRowCount(num_row)
        self.table.setHorizontalHeaderLabels(['ID', 'Family Name', 'Name', 'Father Name', 'Passport_seria', 'Passport_num'])
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

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        scroll = QScrollArea()
        scroll.setWidget(self.table)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
        self.setLayout(layout)

        btnAdd = QPushButton('New client', self)
        btnAdd.resize(QSize(120, 40))
        btnAdd.move(650, 80)
        btnAdd.clicked.connect(self.addNewClient)

        btnMofidy = QPushButton('Modify client', self)
        btnMofidy.resize(QSize(120, 40))
        btnMofidy.move(650, 130)
        btnMofidy.clicked.connect(self.modifyClient)

        btnDelete = QPushButton('Delete client', self)
        btnDelete.resize(QSize(120, 40))
        btnDelete.move(650, 180)
        btnDelete.clicked.connect(self.deleteClient)

        btnBack = QPushButton('Back', self)
        btnBack.resize(QSize(120, 40))
        btnBack.move(650, 450)
        btnBack.clicked.connect(self.backButton)
        self.show()

    def addNewClient(self):
       self.addWindow.initUI(self.table)

    def modifyClient(self):
        self.modWindow.initUI(self.table)

    def deleteClient(self):
        self.delWindow.initUI(self.table)

    def backButton(self):
        self.journalWindow = Journal_win(self.con)
        self.close()

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


class delClientWin(QWidget):
    def __init__(self, con):
        super().__init__()
        self.con = con
        self.CBox = QComboBox(self)

    def initUI(self, table):
        self.table = table
        self.setGeometry(760, 350, 300, 200)
        self.setFixedSize(self.size())
        self.setWindowTitle('Delete client')
        self.setWindowIcon(QIcon(r'C:\Users\shmel\PycharmProjects\DataBase\lib.png'))

        label = QLabel('Client ID:', self)
        label.move(QPoint(60, 50))

        cur = self.con.cursor()
        cur.execute("select id from clients")
        items = []
        for row in cur:
            items.append(str(row[0]))
        self.CBox.addItems(items)
        self.CBox.move(QPoint(170, 60))

        btnGo = QPushButton('Delete', self)
        btnGo.move(QPoint(80, 130))
        btnGo.clicked.connect(self.btnGoClicked)

        self.show()
    
    def btnGoClicked(self):
        cur = self.con.cursor()
        parameters = [self.CBox.currentText()]
        try:
            cur.callproc('PROC_DELETE_CLIENT', parameters)
        except:
            error_d = QMessageBox()
            error_d.setIcon(QMessageBox.Critical)
            error_d.setText("You are not allowed to delete this client")
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


class addBooksWin(QWidget):
    def __init__(self, con):
        super().__init__()
        self.con = con

    def initUI(self, table):
        self.table = table
        self.setGeometry(760, 350, 400, 300)
        self.setFixedSize(self.size())
        self.setWindowTitle('New book')
        self.setWindowIcon(QIcon(r'C:\Users\shmel\PycharmProjects\DataBase\lib.png'))

        l1 = QLabel('Book name:', self)
        l1.move(QPoint(30, 70))
        self.bookNameEdit = QLineEdit(self)
        self.bookNameEdit.move(QPoint(190, 70))

        l2 = QLabel('Count:', self)
        l2.move(30, 120)
        self.countEdit = QLineEdit(self)
        self.countEdit.setValidator(QIntValidator())
        self.countEdit.move(QPoint(190, 120))

        l3 = QLabel('Type:', self)
        l3.move(30, 170)

        cur = self.con.cursor()
        cur.execute("select id, name from book_types")
        items = []
        self.types = dict()
        for row in cur:
            self.types[row[1]] = row[0]
            items.append(row[1])
        self.CBox = QComboBox(self)
        self.CBox.addItems(items)
        self.CBox.move(QPoint(190, 170))

        btnGo = QPushButton('Add', self)
        btnGo.move(QPoint(150, 260))
        btnGo.clicked.connect(self.btnGoClicked)

        self.show()

    def btnGoClicked(self):
        parameters = [self.bookNameEdit.text(), self.countEdit.text(), self.types[self.CBox.currentText()]]
        cur = self.con.cursor()
        if (self.bookNameEdit.text() == '' or self.countEdit.text() == ''):
            error_f = QMessageBox()
            error_f.setIcon(QMessageBox.Critical)
            error_f.setText("Please fill all fields!")
            error_f.setWindowTitle('Error!')
            error_f.exec()
            return
        try:
            cur.callproc('PROC_ADD_NEW_BOOK', parameters)
        except:
            error_d = QMessageBox()
            error_d.setIcon(QMessageBox.Critical)
            error_d.setText("You are not allowed to add this book")
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

class BookTypeWindow(QWidget):
    def __init__(self, con):
        super().__init__()
        self.con = con
        self.addWindow = addBookTypeWin(self.con)
        self.modWindow = modifyBookTypeWin(self.con)
        self.delWindow = delBookTypeWin(self.con)
        self.initUI()

    def initUI(self):
        self.setGeometry(510, 200, 800, 600)
        self.setFixedSize(self.size())
        self.setWindowTitle('Books')
        self.setWindowIcon(QIcon(r'C:\Users\shmel\PycharmProjects\DataBase\lib.png'))

        self.table = QTableWidget(self)
        self.table.setColumnCount(5)
        self.table.setMaximumSize(QSize(620, 550))

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

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        scroll = QScrollArea()
        scroll.setWidget(self.table)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
        self.setLayout(layout)

        btnAdd = QPushButton('Add new book type', self)
        btnAdd.resize(QSize(120, 40))
        btnAdd.move(650, 80)
        btnAdd.clicked.connect(self.addNewType)

        btnMofidy = QPushButton('Modify table', self)
        btnMofidy.resize(QSize(120, 40))
        btnMofidy.move(650, 130)
        btnMofidy.clicked.connect(self.modifyType)

        btnDelete = QPushButton('Delete book type', self)
        btnDelete.resize(QSize(120, 40))
        btnDelete.move(650, 180)
        btnDelete.clicked.connect(self.deleteType)

        btnBack = QPushButton('Back', self)
        btnBack.resize(QSize(120, 40))
        btnBack.move(650, 450)
        btnBack.clicked.connect(self.backButton)

        self.show()

    def addNewType(self):
       self.addWindow.initUI(self.table)

    def modifyType(self):
        self.modWindow.initUI(self.table)

    def deleteType(self):
        self.delWindow.initUI(self.table)

    def backButton(self):
        self.journalWindow = Journal_win(self.con)
        self.close()


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


class delBookTypeWin(QWidget):
    def __init__(self, con):
        super().__init__()
        self.con = con

    def initUI(self, table):
        self.table = table
        self.setGeometry(760, 350, 300, 200)
        self.setFixedSize(self.size())
        self.setWindowTitle('Delete book type')
        self.setWindowIcon(QIcon(r'C:\Users\shmel\PycharmProjects\DataBase\lib.png'))

        l1 = QLabel('Type ID:', self)
        l1.move(50, 62)

        cur = self.con.cursor()
        cur.execute("select id from book_types")
        Items = []
        for row in cur:
            Items.append(str(row[0]))
        self.CBox = QComboBox(self)
        self.CBox.addItems(Items)
        self.CBox.move(170, 60)

        btnGo = QPushButton('Delete', self)
        btnGo.move(QPoint(80, 130))
        btnGo.clicked.connect(self.btnGoClicked)

        self.show()

    def btnGoClicked(self):
        cur = self.con.cursor()
        parameters = [self.CBox.currentText()]
        try:
            cur.callproc('PROC_DELETE_BOOK_TYPE', parameters)
        except:
            error_d = QMessageBox()
            error_d.setIcon(QMessageBox.Critical)
            error_d.setText("You are not allowed to delete this book type")
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

class ReturnBookWindow(QWidget):
    def __init__(self, con):
        super().__init__()
        self.con = con

    def initUI(self, table):
        self.table = table
        self.setGeometry(760, 350, 400, 300)
        self.setFixedSize(self.size())
        self.setWindowTitle('New return')
        self.setWindowIcon(QIcon(r'C:\Users\shmel\PycharmProjects\DataBase\lib.png'))


        l1 = QLabel('ID: ', self)
        l1.move(QPoint(30, 70))
        cur = self.con.cursor()
        cur.execute("select id from journal")
        items = []
        for row in cur:
            items.append(str(row[0]))
        self.CBox_1 = QComboBox(self)
        self.CBox_1.addItems(items)
        self.CBox_1.move(QPoint(190, 70))

        l2 = QLabel('Date: ', self)
        l2.move(QPoint(30, 120))
        self.dateEdit = QLineEdit(self)
        re = QRegExp(r'[0-9]{4}/{1}[0-9]{2}/{1}[0-9]{2}')
        myValidator = QRegExpValidator(re, self.dateEdit)
        self.dateEdit.setValidator(myValidator)
        self.dateEdit.move(190, 120)

        btnGo = QPushButton('Submit', self)
        btnGo.move(QPoint(150, 260))
        btnGo.clicked.connect(self.btnGoClicked)

        self.show()

    def btnGoClicked(self):
        parameters = [self.CBox_1.currentText(), self.dateEdit.text()]
        print(parameters)
        cur = self.con.cursor()
        try:
            cur.callproc('PROC_GET_BORROWED_BOOK', parameters)
        except:
            error_d = QMessageBox()
            error_d.setIcon(QMessageBox.Critical)
            error_d.setText("Date is not correct. Please check!")
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


