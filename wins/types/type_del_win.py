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