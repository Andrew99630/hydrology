import math

from PyQt5 import QtWidgets, QtCore, QtSql

from spring_flood_design import Ui_MainWindow

PARAMETERS = ['A', 'Lesistost', 'Zabolochennost', 'Ozernost', 'Istok']
PARAMETERS_Q = ['QP0', 'QP1', 'QP2', 'QP5', 'QP10', 'QP25']
PARAMETERS_H = ['HP0', 'HP1', 'HP2', 'HP5', 'HP10', 'HP25']
PARAMETERS_P = ['P0', 'P1', 'P2', 'P5', 'P10', 'P25']


class Spring_flood(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.query = QtSql.QSqlQuery()
        self.query.exec("SELECT Name FROM Verhnyaya_Volga")
        self.query.first()
        while self.query.isValid():
            self.comboBox_river1.addItem(self.query.value('Name'))
            self.comboBox_river2.addItem(self.query.value('Name'))
            self.comboBox_river3.addItem(self.query.value('Name'))
            self.query.next()
        self.query.finish()
        self.query.prepare("SELECT Istok, A, Ozernost, Zabolochennost, Lesistost FROM Verhnyaya_Volga WHERE Name = ?")
        self.query.addBindValue(self.comboBox_river1.currentText())
        self.query.exec_()
        self.query.first()
        for row in range(0, 5):
            self.model_tableriver1.setData(self.model_tableriver1.index(row, 2), self.query.value(PARAMETERS[row]))
        self.table_river1.resizeColumnsToContents()
        self.comboBox_analog.currentIndexChanged[str].connect(self.count_river)
        self.pushButton_accept.clicked.connect(self.accept)
        self.pushButton_clear.clicked.connect(self.clear)
        self.lineEdit_river1.textEdited.connect(lambda x: self.search(self.lineEdit_river1.text(), 1))
        self.lineEdit_river2.textEdited.connect(lambda x: self.search(self.lineEdit_river2.text(), 2))
        self.lineEdit_river3.textEdited.connect(lambda x: self.search(self.lineEdit_river3.text(), 3))
        self.comboBox.currentIndexChanged[str].connect(self.recommendations)
        self.comboBox_river1.currentIndexChanged[str].connect(lambda x: self.rivername_changed(1))
        self.comboBox_river2.currentIndexChanged[str].connect(lambda x: self.rivername_changed(2))
        self.comboBox_river3.currentIndexChanged[str].connect(lambda x: self.rivername_changed(3))
        self.model_tableriver1.setData(self.model_tableriver2.index(5, 2), 7)
        self.model_tableriver1.setData(self.model_tableriver2.index(6, 2), 15)

    def count_river(self, number):
        number = int(number)
        for i in range(number + 1, 4):
            getattr(self, 'comboBox_river%s' % i).hide()
            getattr(self, 'lineEdit_river%s' % i).hide()
            getattr(self, 'label%s' % i).hide()
        for i in range(1, number + 1):
            getattr(self, 'comboBox_river%s' % i).show()
            getattr(self, 'lineEdit_river%s' % i).show()
            getattr(self, 'label%s' % i).show()
            self.model_tableriver1.setColumnCount(i + 2)
        if number == 1:
            self.model_tableriver1.setHorizontalHeaderLabels(['Характеристика', 'Единицы измерения', 'Водоём 1'])
            for row in range(8, 20):
                self.table_river2.hideRow(row)
        elif number == 2:
            self.model_tableriver1.setHorizontalHeaderLabels(
                ['Характеристика', 'Единицы измерения', 'Водоём 1', 'Водоём 2'])
            for row in range(8, 14):
                self.table_river2.showRow(row)
                self.table_river2.hideRow(row + 6)
            self.model_tableriver2.item(8, 0).setTextAlignment(QtCore.Qt.AlignCenter)
        else:
            self.model_tableriver1.setHorizontalHeaderLabels(
                ['Характеристика', 'Единицы измерения', 'Водоём 1', 'Водоём 2', 'Водоём 3'])
            for row in range(8, 20):
                self.table_river2.showRow(row)
            self.model_tableriver2.item(8, 0).setTextAlignment(QtCore.Qt.AlignCenter)
            self.model_tableriver2.item(14, 0).setTextAlignment(QtCore.Qt.AlignCenter)
        self.table_river2.resizeColumnsToContents()
        for col in range(2, self.model_tableriver1.columnCount()):
            name = getattr(self, 'comboBox_river%s' % number).currentText()
            self.query.prepare(
                "SELECT Istok, A, Ozernost, Zabolochennost, Lesistost FROM Verhnyaya_Volga WHERE Name = ?")
            self.query.addBindValue(name)
            self.query.exec_()
            self.query.first()
            for row in range(0, 5):
                self.model_tableriver1.setData(self.model_tableriver1.index(row, col), self.query.value(PARAMETERS[row]))
            self.query.finish()

    def rivername_changed(self, number):
        name = getattr(self, 'comboBox_river%s' % number).currentText()
        self.query.prepare("SELECT Istok, A, Ozernost, Zabolochennost, Lesistost FROM Verhnyaya_Volga WHERE Name = ?")
        self.query.addBindValue(name)
        self.query.exec_()
        self.query.first()
        for row in range(0, 5):
            self.model_tableriver1.setData(self.model_tableriver1.index(row, number + 1), self.query.value(PARAMETERS[row]))
        self.query.finish()

    def clear(self):
        self.table_stvor1.setItem(7, 2, QtWidgets.QTableWidgetItem(''))
        self.table_stvor1.setItem(8, 2, QtWidgets.QTableWidgetItem(''))
        self.spin_river5.setValue(0)
        self.spin_river6.setValue(0)
        for row in range(0, 7):
            getattr(self, 'spin_stvor%s' % row).setValue(0)
        column_count = self.model_tableriver1.columnCount()
        for row in range(0, 9):
            for col in range(2, column_count):
                self.model_tableriver1.setData(self.model_tableriver1.index(row, col), '')
        for row in range(2, 8):
            for col in range(2, 16):
                self.model_tablestvor2.setData(self.model_tablestvor2.index(row, col), '')
            for col in range(2, 14):
                self.model_tableriver.setData(self.model_tableriver.index(row, col), '')

    def accept(self):
        try:
            self.filling_tableriver1()
            self.filling_tableriver2()
            self.filling_tablestvor1()
            self.filling_tablestvor2()
        except:
            QtWidgets.QMessageBox.critical(self, 'Ошибка', 'Проверьте корректность введённых данных',
                                           defaultButton=QtWidgets.QMessageBox.Ok)

    def filling_tableriver1(self):
        for col in range(2, self.model_tableriver1.columnCount()):
            self.query.prepare(
                "SELECT Istok, A, Ozernost, Zabolochennost, Lesistost FROM Verhnyaya_Volga WHERE Name = ?")
            self.query.addBindValue(getattr(self, 'comboBox_river%s' % (col - 1)).currentText())
            self.query.exec_()
            self.query.first()
            self.model_tableriver1.setData(self.model_tableriver1.index(0, col), self.query.value('A'))
            self.model_tableriver1.setData(self.model_tableriver1.index(1, col), self.query.value('Lesistost'))
            self.model_tableriver1.setData(self.model_tableriver1.index(2, col), self.query.value('Zabolochennost'))
            self.model_tableriver1.setData(self.model_tableriver1.index(3, col), self.query.value('Ozernost'))
            self.model_tableriver1.setData(self.model_tableriver1.index(4, col), self.query.value('Istok'))
            self.model_tableriver1.setData(self.model_tableriver1.index(7, col),
                                           self.query.value('Istok') / (self.query.value('A') ** 0.56))
            self.model_tableriver1.setData(self.model_tableriver1.index(8, col),
                                           float((self.spin_river6.value())) * (self.query.value('A') ** 0.5))

    def filling_tableriver2(self):
        for row in range(2, 20):
            for col in range(2, 13):
                self.model_tableriver2.setData(self.model_tableriver2.index(row, col), '')
        self.QAh_river()
        self.u_river()
        self.b_river()
        self.b1_river()
        self.b2_river()
        self.n_river()
        self.k_river()
        self.table_river2.resizeColumnsToContents()

    def QAh_river(self):
        for i in range(1, self.model_tableriver1.columnCount() - 1):
            self.query.prepare(
                "SELECT A, QP0, QP1, QP2, QP5, QP10, QP25, HP0, HP1, HP2, HP5, HP10, HP25 "
                "FROM Verhnyaya_Volga WHERE Name = ?")
            self.query.addBindValue(getattr(self, 'comboBox_river%s' % i).currentText())
            self.query.exec_()
            self.query.first()
            r = 2
            while self.model_tableriver2.data(self.model_tableriver2.index(r, 2)):
                r += 1
            for row in range(r, r + 6):
                self.model_tableriver2.setData(self.model_tableriver2.index(row, 2), self.query.value(PARAMETERS_Q[row - r]))
                self.model_tableriver2.setData(self.model_tableriver2.index(row, 3), self.query.value(PARAMETERS_H[row - r]))
                self.model_tableriver2.setData(self.model_tableriver2.index(row, 8), self.query.value('A'))
            self.query.finish()

    def u_river(self):
        for i in range(1, self.model_tableriver1.columnCount() - 1):
            self.query.prepare("SELECT P0, P1, P2, P5, P10, P25 FROM Zone_y WHERE Zone = ?")
            self.query.addBindValue(getattr(self, 'comboBox_rzone%s' % i).currentText())
            self.query.exec_()
            self.query.first()
            r = 2
            while self.model_tableriver2.data(self.model_tableriver2.index(r, 4)):
                r += 1
            for row in range(r, r + 6):
                self.model_tableriver2.setData(self.model_tableriver2.index(row, 4), self.query.value(PARAMETERS_P[row - r]))
            self.query.finish()

    def b_river(self):
        for i in range(1, self.model_tableriver1.columnCount() - 1):
            ozernost = int(self.model_tableriver1.data(self.model_tableriver1.index(3, i + 1)))
            A = float(self.model_tableriver1.data(self.model_tableriver1.index(0, i + 1)))
            Ao = (getattr(self, 'spin_lsquare%s' % i).value() * 100 * getattr(self, 'spin_la%s' % i).value()) / A
            r = 2
            while self.model_tableriver2.data(self.model_tableriver2.index(r, 5)):
                r += 1
            if getattr(self, 'comboBox_rlake%s' % i).currentText() == 'Нет':
                if ozernost == 0 or Ao < 2:
                    for row in range(r, r + 6):
                        self.model_tableriver2.setData(self.model_tableriver2.index(row, 5), 1)
                elif Ao >= 2:
                    for row in range(r, r + 6):
                        self.model_tableriver2.setData(self.model_tableriver2.index(row, 5), 0.8)
            else:
                b = 1 / (1 + Ao * 0.3)
                for row in range(r, r + 6):
                    self.model_tableriver2.setData(self.model_tableriver2.index(row, 5), round(b, 2))

    def b1_river(self):
        for i in range(1, self.model_tableriver1.columnCount() - 1):
            ozernost = int(self.model_tableriver1.data(self.model_tableriver1.index(3, i + 1)))
            lesistost = int(self.model_tableriver1.data(self.model_tableriver1.index(1, i + 1)))
            r = 2
            while self.model_tableriver2.data(self.model_tableriver2.index(r, 6)):
                r += 1
            if lesistost < 3 or ozernost > 20:
                for row in range(r, r + 6):
                    self.model_tableriver2.setData(self.model_tableriver2.index(row, 6), 1)
            else:
                An = None
                if 3 <= lesistost <= 9:
                    An = '3-9'
                elif 10 <= lesistost <= 19:
                    An = '10-19'
                elif 20 <= lesistost <= 30:
                    An = '20-30'
                elif 31 <= lesistost <= 99:
                    An = '30+'
                self.query.prepare("SELECT a1 FROM Forest_place WHERE Zone = ? AND Location = ? AND An = ?")
                self.query.bindValue(0, getattr(self, 'comboBox_rzone%s' % i).currentText())
                self.query.bindValue(1, getattr(self, 'comboBox_rforest%s' % i).currentText())
                self.query.bindValue(2, An)
                self.query.exec_()
                self.query.first()
                a1 = self.query.value('a1')
                self.query.finish()
                self.query.prepare("SELECT n FROM Grunt WHERE Zone = ? AND Grunt = ?")
                self.query.bindValue(0, getattr(self, 'comboBox_rzone%s' % i).currentText())
                self.query.bindValue(1, getattr(self, 'comboBox_rgrunt%s' % i).currentText())
                self.query.exec_()
                self.query.first()
                n = self.query.value('n')
                self.query.finish()
                b1 = round((a1 / (lesistost + 1) ** n), 2)
                for row in range(r, r + 6):
                    self.model_tableriver2.setData(self.model_tableriver2.index(row, 6), round(b1, 2))

    def b2_river(self):
        for i in range(1, self.model_tableriver1.columnCount() - 1):
            self.query.prepare("SELECT A, Ozernost, Zabolochennost FROM Verhnyaya_Volga WHERE Name = ?")
            self.query.addBindValue(getattr(self, 'comboBox_river%s' % i).currentText())
            self.query.exec_()
            self.query.first()
            ozernost = int(self.model_tableriver1.data(self.model_tableriver1.index(3, i + 1)))
            zabolochennost = int(self.model_tableriver1.data(self.model_tableriver1.index(2, i + 1)))
            r = 2
            while self.model_tableriver2.data(self.model_tableriver2.index(r, 7)):
                r += 1
            if zabolochennost < 3 or ozernost > 20:
                for row in range(r, r + 6):
                    self.model_tableriver2.setData(self.model_tableriver2.index(row, 7), 1)
            else:
                self.query.prepare("SELECT Beta FROM Index_beta WHERE Type = ?")
                self.query.addBindValue(getattr(self, 'comboBox_rswamp%s' % i).currentText())
                self.query.exec_()
                self.query.first()
                beta = self.query.value('Beta')
                self.query.finish()
                b2 = 1 - beta * math.log10(0.1 * zabolochennost + 1)
                for row in range(r, r + 6):
                    self.model_tableriver2.setData(self.model_tableriver2.index(row, 7), round(b2, 2))

    def n_river(self):
        for i in range(1, self.model_tableriver1.columnCount() - 1):
            self.query.prepare("SELECT n1, A1 FROM Reduction WHERE Zone = ?")
            self.query.addBindValue(getattr(self, 'comboBox_rzone%s' % i).currentText())
            self.query.exec_()
            self.query.first()
            n1 = self.query.value('n1')
            A1 = self.query.value('A1')
            self.query.finish()
            r = 2
            while self.model_tableriver2.data(self.model_tableriver2.index(r, 9)):
                r += 1
            for row in range(r, r + 6):
                self.model_tableriver2.setData(self.model_tableriver2.index(row, 9), A1)
                self.model_tableriver2.setData(self.model_tableriver2.index(row, 10), n1)
                self.model_tableriver2.setData(self.model_tableriver2.index(row, 11), round(
                    ((A1 + float(self.model_tableriver2.data(self.model_tableriver2.index(r, 8)))) ** n1), 2))

    def k_river(self):
        for i in range(1, self.model_tableriver1.columnCount() - 1):
            r = 2
            while self.model_tableriver2.data(self.model_tableriver2.index(r, 12)):
                r += 1
            for row in range(r, r + 6):
                Q = float(self.model_tableriver2.data(self.model_tableriver2.index(row, 2)))
                h = float(self.model_tableriver2.data(self.model_tableriver2.index(row, 3)))
                u = float(self.model_tableriver2.data(self.model_tableriver2.index(row, 4)))
                b = float(self.model_tableriver2.data(self.model_tableriver2.index(row, 5)))
                b1 = float(self.model_tableriver2.data(self.model_tableriver2.index(row, 6)))
                b2 = float(self.model_tableriver2.data(self.model_tableriver2.index(row, 7)))
                A = float(self.model_tableriver2.data(self.model_tableriver2.index(row, 8)))
                An = float(self.model_tableriver2.data(self.model_tableriver2.index(row, 11)))
                K = (Q * An) / (h * u * b * b1 * b2 * A)
                self.model_tableriver2.setData(self.model_tableriver2.index(row, 12), round(K, 3))

    def filling_tablestvor1(self):
        if self.spin_stvor0.value() and self.spin_stvor4.value() and self.spin_stvor5.value() and self.spin_stvor6.value():
            x = round(self.spin_stvor4.value() / (self.spin_stvor0.value() ** 0.56), 2)
            y = round(self.spin_stvor6.value() * (self.spin_stvor0.value() ** 0.5), 2)
            self.table_stvor1.setItem(7, 2, QtWidgets.QTableWidgetItem(str(x)))
            self.table_stvor1.setItem(8, 2, QtWidgets.QTableWidgetItem(str(y)))
        else:
            QtWidgets.QMessageBox.critical(self, 'Ошибка', 'Проверьте корректность введённых данных об исследуемом водотоке',
                                           defaultButton=QtWidgets.QMessageBox.Ok)

    def filling_tablestvor2(self):
        self.b_stvor()
        self.b1_stvor()
        self.b2_stvor()
        self.u_n_stvor()
        self.k_stvor()
        self.CvCs_stvor()
        self.h_stvor()
        self.Q_stvor()
        self.table_stvor2.resizeColumnsToContents()

    def b_stvor(self):
        ozernost = self.spin_stvor3.value()
        coefficient_dict = {'Лесная и тундра': 0.2, 'Лесостепная': 0.2, 'Степная': 0.4}
        c = coefficient_dict[self.comboBox_zone.currentText()]
        A = self.spin_stvor0.value()
        Ao = (self.spin_lsquare.value() * 100 * self.spin_la.value()) / A
        if self.comboBox_lake.currentText() == 'Нет':
            if ozernost == 0 or Ao < 2:
                for row in range(2, 8):
                    self.model_tablestvor2.setData(self.model_tablestvor2.index(row, 5), 1)
            elif Ao >= 2:
                for row in range(2, 8):
                    self.model_tablestvor2.setData(self.model_tablestvor2.index(row, 5), 0.8)
        elif self.comboBox_lake.currentText() == 'Да':
            b = 1 / (1 + Ao * c)
            for row in range(2, 8):
                self.model_tablestvor2.setData(self.model_tablestvor2.index(row, 5), round(b, 2))

    def b1_stvor(self):
        ozernost = self.spin_stvor3.value()
        lesistost = self.spin_stvor1.value()
        if lesistost < 3 or ozernost > 20:
            for row in range(2, 8):
                self.model_tablestvor2.setData(self.model_tablestvor2.index(row, 6), 1)
        else:
            An = None
            if 3 <= lesistost <= 9:
                An = '3-9'
            elif 10 <= lesistost <= 19:
                An = '10-19'
            elif 20 <= lesistost <= 30:
                An = '20-30'
            elif 31 <= lesistost <= 99:
                An = '30+'
            self.query.prepare("SELECT a1 FROM Forest_place WHERE Zone = ? AND Location = ? AND An = ?")
            self.query.bindValue(0, self.comboBox_zone.currentText())
            self.query.bindValue(1, self.comboBox_forest.currentText())
            self.query.bindValue(2, An)
            self.query.exec_()
            self.query.first()
            a1 = self.query.value('a1')
            self.query.finish()
            self.query.prepare("SELECT n FROM Grunt WHERE Zone = ? AND Grunt = ?")
            self.query.bindValue(0, self.comboBox_zone.currentText())
            self.query.bindValue(1, self.comboBox_grunt.currentText())
            self.query.exec_()
            self.query.first()
            n = self.query.value('n')
            self.query.finish()
            b1 = round((a1 / (lesistost + 1) ** n), 2)
            for row in range(2, 8):
                self.model_tablestvor2.setData(self.model_tablestvor2.index(row, 6), round(b1, 2))

    def b2_stvor(self):
        ozernost = self.spin_stvor3.value()
        zabolochennost = self.spin_stvor2.value()
        A = self.spin_stvor0.value()
        if zabolochennost < 3 or ozernost > 20:
            for row in range(2, 8):
                self.model_tablestvor2.setData(self.model_tablestvor2.index(row, 7), 1)
        else:
            self.query.prepare("SELECT Beta FROM Index_beta WHERE Type = ?")
            self.query.addBindValue(self.comboBox_swamp.currentText())
            self.query.exec_()
            self.query.first()
            beta = self.query.value('Beta')
            self.query.finish()
            b2 = 1 - beta * math.log10(0.1 * zabolochennost + 1)
            for row in range(2, 8):
                self.model_tablestvor2.setData(self.model_tablestvor2.index(row, 7), round(b2, 2))
        for row in range(2, 8):
            self.model_tablestvor2.setData(self.model_tablestvor2.index(row, 8), A)

    def u_n_stvor(self):
        self.query.prepare("SELECT P0, P1, P2, P5, P10, P25 FROM Zone_y WHERE Zone = ?")
        self.query.addBindValue(self.comboBox_zone.currentText())
        self.query.exec_()
        self.query.first()
        for row in range(2, 8):
            self.model_tablestvor2.setData(self.model_tablestvor2.index(row, 4), self.query.value(PARAMETERS_P[row - 2]))
        self.query.finish()
        self.query.prepare("SELECT n1, A1 FROM Reduction WHERE Zone = ?")
        self.query.addBindValue(self.comboBox_zone.currentText())
        self.query.exec_()
        self.query.first()
        n1 = self.query.value('n1')
        A1 = self.query.value('A1')
        self.query.finish()
        new_square = round(A1 + self.spin_stvor0.value() ** n1, 2)
        for row in range(2, 8):
            self.model_tablestvor2.setData(self.model_tablestvor2.index(row, 9), A1)
            self.model_tablestvor2.setData(self.model_tablestvor2.index(row, 10), n1)
            self.model_tablestvor2.setData(self.model_tablestvor2.index(row, 11), new_square)

    def k_stvor(self):
        if self.model_tableriver1.columnCount() == 3:
            for row in range(2, 8):
                K = self.model_tableriver2.data(self.model_tableriver2.index(row, 12))
                self.model_tablestvor2.setData(self.model_tablestvor2.index(row, 12), round(K, 3))
        elif self.model_tableriver1.columnCount() == 4:
            for row in range(2, 8):
                K = (self.model_tableriver2.data(self.model_tableriver2.index(row, 12)) + self.model_tableriver2.data(
                    self.model_tableriver2.index(row + 6, 12))) / 2
                self.model_tablestvor2.setData(self.model_tablestvor2.index(row, 12), round(K, 3))
        elif self.model_tableriver1.columnCount() == 5:
            for row in range(2, 8):
                K = (self.model_tableriver2.data(self.model_tableriver2.index(row, 12)) + self.model_tableriver2.data(
                    self.model_tableriver2.index(row + 6, 12)) + self.model_tableriver2.data(
                    self.model_tableriver2.index(row + 12, 12))) / 3
                self.model_tablestvor2.setData(self.model_tablestvor2.index(row, 12), round(K, 3))

    def CvCs_stvor(self):
        Cv = self.spin_cv.value()
        CvCs = str(self.combo_cvcs.currentText())
        A = self.spin_stvor0.value()
        if A <= 50:
            Cv = round(Cv * 1.25, 2)
        elif 50 < A <= 100:
            Cv = round(Cv * 1.23, 2)
        elif 100 < A <= 150:
            Cv = round(Cv * 1.17, 2)
        elif A <= 200:
            Cv = round(Cv * 1.1, 2)
        else:
            Cv = round(Cv, 2)
        for row in range(2, 8):
            self.model_tablestvor2.setData(self.model_tablestvor2.index(row, 13), Cv)
            self.model_tablestvor2.setData(self.model_tablestvor2.index(row, 14), CvCs)

    def h_stvor(self):
        CvCs = float(self.model_tablestvor2.data(self.model_tablestvor2.index(2, 14)))
        Cv = float(self.model_tablestvor2.data(self.model_tablestvor2.index(2, 13)))
        k1 = round(Cv, 1)
        k2 = 0
        if Cv < k1:
            k2 = k1 - 0.1
        elif Cv > k1:
            k2 = k1 + 0.1
        elif Cv == k1:
            k2 = 0
        probability = [0.1, 1, 2, 5, 10, 25]
        for row in range(2, 8):
            if CvCs == 2:
                self.query.prepare("SELECT * FROM Variation2 WHERE P = ?")
            elif CvCs == 3:
                self.query.prepare("SELECT * FROM Variation3 WHERE P = ?")
            self.query.bindValue(0, str(probability[row - 2]))
            self.query.exec_()
            self.query.first()
            x2 = 0
            x1 = float(self.query.value(str(k1)))
            if k2:
                x2 = float(self.query.value(str(k2)))
            elif k2 == 0:
                x2 = 0
            self.query.finish()
            k = 0
            if x2 == 0:
                k = x1
            else:
                if x1 > x2:
                    if k1 > k2:
                        k = x1 - (((x1 - x2) / 10) * (k1 - Cv) * 100)
                    else:
                        k = x1 - (((x1 - x2) / 10) * (k2 - Cv) * 100)
                elif x1 < x2:
                    if k1 > k2:
                        k = x2 - ((x2 - x1) / 10) * (k1 - Cv) * 100
                    else:
                        k = x2 - ((x2 - x1) / 10) * (k2 - Cv) * 100
            h = k * self.spin_h.value()
            self.model_tablestvor2.setData(self.model_tablestvor2.index(row, 3), h)

    def Q_stvor(self):
        for row in range(2, 8):
            K = self.model_tablestvor2.data(self.model_tablestvor2.index(row, 12))
            h = self.model_tablestvor2.data(self.model_tablestvor2.index(row, 3))
            u = float(self.model_tablestvor2.data(self.model_tablestvor2.index(row, 4)))
            b = self.model_tablestvor2.data(self.model_tablestvor2.index(row, 5))
            b1 = self.model_tablestvor2.data(self.model_tablestvor2.index(row, 6))
            b2 = self.model_tablestvor2.data(self.model_tablestvor2.index(row, 7))
            A = self.model_tablestvor2.data(self.model_tablestvor2.index(row, 8))
            An = self.model_tablestvor2.data(self.model_tablestvor2.index(row, 11))
            Q = (K * h * u * b * b1 * b2 * A) / An
            self.model_tablestvor2.setData(self.model_tablestvor2.index(row, 2), round(Q, 2))

    def recommendations(self, text):
        names = []
        for i in range(1, 4):
            getattr(self, 'comboBox_river%s' % i).clear()
        if text == 'Да':
            self.query.prepare("SELECT Name FROM  Verhnyaya_Volga WHERE Istok BETWEEN ? AND ? AND A BETWEEN ? AND ?")
            self.query.bindValue(0, self.spin_square_3.value())
            self.query.bindValue(1, self.spin_square_4.value())
            self.query.bindValue(2, self.spin_square_1.value())
            self.query.bindValue(3, self.spin_square_2.value())
            self.query.exec_()
            self.query.first()
            while self.query.isValid():
                names.append(self.query.value('Name'))
                self.query.next()
            self.query.finish()
        elif text == 'Нет':
            self.query.exec("SELECT Name FROM Verhnyaya_Volga")
            self.query.first()
            while self.query.isValid():
                names.append(self.query.value('Name'))
                self.query.next()
            self.query.finish()
        self.comboBox_river1.addItems(names)
        self.comboBox_river2.addItems(names)
        self.comboBox_river3.addItems(names)

    def search(self, text, number):
        names = []
        if getattr(self, 'lineEdit_river%s' % number).text():
            getattr(self, 'comboBox_river%s' % number).clear()
            self.query.prepare("SELECT Name FROM Verhnyaya_Volga WHERE Name LIKE ?")
            word = '%' + text + '%'
            print(word)
            self.query.addBindValue(word)
            self.query.exec_()
            self.query.first()
            while self.query.isValid():
                names.append(self.query.value('Name'))
                self.query.next()
            self.query.finish()
        else:
            getattr(self, 'comboBox_river%s' % number).clear()
            self.query.exec("SELECT Name FROM Verhnyaya_Volga")
            self.query.first()
            while self.query.isValid():
                names.append(self.query.value('Name'))
                self.query.next()
            self.query.finish()
        getattr(self, 'comboBox_river%s' % number).addItems(names)