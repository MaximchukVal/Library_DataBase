import connector as con
import sys
import wins.entry_win as ent

from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    enterWindow = ent.enterWindow(con)
    sys.exit(app.exec_())
