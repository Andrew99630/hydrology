import sys

from PyQt5 import QtWidgets, QtSql
from spring_flood import Spring_flood

conn = QtSql.QSqlDatabase.addDatabase('QSQLITE')
conn.setDatabaseName('Hydro.db')
conn.open()

class Main_window(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.tab = QtWidgets.QTabWidget()
        self.tab.addTab(Spring_flood(), 'Весеннее половодье')
        self.tab.setCurrentIndex(0)
        self.box = QtWidgets.QVBoxLayout()
        self.box.addWidget(self.tab)
        self.setLayout(self.box)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    hydro = Main_window()
    hydro.setWindowTitle('Расчёт уровней воды весеннего половодья и дождевых паводков при отсутствии наблюдений')
    hydro.setFixedSize(1850, 840)
    hydro.show()
    sys.exit(app.exec_())