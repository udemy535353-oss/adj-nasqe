import sqlite3
import sys
import os
import time
from PyQt5 import QtWidgets
import random
import string
class pencere(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.bağlantı()
        self.init_ui()
    def bağlantı(self):
        self.con = sqlite3.connect("retret.db")
        self.cursor = self.con.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS libm(numara TEXT)")
        self.con.commit()
    def rasgele(self,uzunluk = 10):
        karakter = string.digits
        kod = "".join(random.choice(karakter) for b in range(uzunluk))
        return kod
    def init_ui(self):
        self.test = QtWidgets.QPushButton("tıkal")
        v = QtWidgets.QVBoxLayout()
        v.addWidget(self.test)
        h = QtWidgets.QHBoxLayout()
        h.addStretch()
        h.addLayout(v)
        h.addStretch()
        self.setLayout(h)
        self.show()
        self.test.clicked.connect(self.laplap)
    def laplap(self):
        hak = 0
        while (hak < 999):
            num = self.rasgele()
            self.cursor.execute("select numara from libm where numara = ?", (num,))
            data = self.cursor.fetchall()
            if len(data) == 0 and num.startswith("0516"):
                self.cursor.execute("insert into libm values(?)",(num,))
                self.con.commit()
                return

            else:
                hak += 1

        
        
app = QtWidgets.QApplication(sys.argv)
pencere = pencere()
sys.exit(app.exec_())