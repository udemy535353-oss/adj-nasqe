import sqlite3
import sys
import os
import time
from PyQt5 import QtWidgets
import random
class pencere(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.bağlantı()
        self.init_ui()
    def bağlantı(self):
        self.con = sqlite3.connect("okul.db")
        self.cursor = self.con.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS helikopter(kullanıcı TEXT,şifre TEXT)")
        self.con.commit()
    def init_ui(self):
        self.ad = QtWidgets.QLineEdit("kullanıcı adı girin")
        self.şifre = QtWidgets.QLineEdit("şifre girin")
        self.şifre.setEchoMode(QtWidgets.QLineEdit.Password)
        self.yazı = QtWidgets.QLabel("hesabınıza giriş yapın")
        self.giriş = QtWidgets.QPushButton("Giriş")
        self.kaydol = QtWidgets.QPushButton("Kaydol")
        v = QtWidgets.QVBoxLayout()
        v.addWidget(self.ad)
        v.addWidget(self.şifre)
        v.addWidget(self.yazı)
        v.addWidget(self.giriş)
        v.addWidget(self.kaydol)
        v.addStretch()
        h = QtWidgets.QHBoxLayout()
        h.addStretch()
        h.addLayout(v)
        h.addStretch()
        self.setLayout(h)
        self.setWindowTitle("test3446")
        self.show()
        self.giriş.clicked.connect(self.gir)
        self.kaydol.clicked.connect(self.sign)
    def gir(self):
        kullanıcıb = self.ad.text()
        şifrer = self.şifre.text()
        self.cursor.execute("SELECT * FROM helikopter WHERE kullanıcı = ? AND şifre = ?",((kullanıcıb,şifrer)))
        data = self.cursor.fetchall()
        if kullanıcıb == "" or şifrer == "":
            self.yazı.setText("boş alanları doldurun")
        elif len(data) == 0:
            self.yazı.setText("Böyle bir hesap yok")
        elif len(kullanıcıb) < 8 or len(şifrer) < 8:
            self.yazı.setText("daha uzun girin")
        else:
            self.yazı.setText("gireiş başarılı") 
    def sign(self):
        kullanıcı = self.ad.text()
        şifre = self.şifre.text()
        self.cursor.execute("select kullanıcı from helikopter")
        moe = self.cursor.fetchall()
        if kullanıcı == "" or şifre == "":
            self.yazı.setText("boş alanları doldur")
        elif len(kullanıcı) < 8 or len(şifre) < 8:
            self.yazı.setText("bu kadar kısa olamaz")
            return
        for b in moe:
            s = b[0]
            if kullanıcı == s:
                self.yazı.setText("böyle bir kullanıcı var")
                return
        else:
            self.yazı.setText("kayıt yapılıyor...")
            time.sleep(2)
            self.yazı.setText("kayıt başarılı")
            self.cursor.execute("Insert into helikopter Values(?,?)",(kullanıcı,şifre))
            self.con.commit()


app = QtWidgets.QApplication(sys.argv)
pencere = pencere()
sys.exit(app.exec_())