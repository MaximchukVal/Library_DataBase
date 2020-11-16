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