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