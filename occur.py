from PyQt5.QtWidgets import QMainWindow,QLabel, QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
import string
import random
import sys
import sqlite3
class mobile(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 400)
        self.bağlantı()
        self.init_ui()

    def bağlantı(self):
        self.con = sqlite3.connect("ua.db")
        self.cursor = self.con.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS lib(numara TEXT)")
        self.con.commit()
    def create(self,uzunluk = 11):
        karakter = string.digits
        kod = "".join(random.choice(karakter) for b in range(uzunluk))
        return kod
    def init_ui(self):
        self.launch = QtWidgets.QPushButton("Check")
        self.launch.setObjectName("QPushButton")
        self.sorgu = QtWidgets.QLineEdit()
        self.sorgu.setFixedSize(180, 35)
        self.sorgu.setStyleSheet("background-color: #544d4d;")
        self.sorgu.setFixedSize(100,30)
        self.sorgu.setObjectName("queryInput")
        self.yazı = QLabel("")
        self.yazı.setWordWrap(True)
        self.buton = QtWidgets.QPushButton("Launch")
        self.buton.setObjectName("generateButton")
        self.view = QtWidgets.QPushButton("view")
        self.view.setObjectName("viewButton")
        self.message = QLabel("uygulamaya hoşgeldiniz")
        self.message.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.message.setWordWrap(True)
        self.message.setObjectName("messageLabel")
        self.h = QtWidgets.QHBoxLayout()
        self.h.addWidget(self.sorgu)
        self.h.addStretch(1)
        self.v = QtWidgets.QVBoxLayout()
        self.v.addLayout(self.h)
        self.v.addWidget(self.message)
        self.grid = QtWidgets.QGridLayout()
        self.grid.addWidget(self.launch, 0, 0)
        self.grid.addWidget(self.view, 0, 1)
        self.grid.addWidget(self.buton, 0, 2)
        self.v.addLayout(self.grid)
        self.setLayout(self.v)

        self.setWindowTitle("Test UPP")
        self.show()
        self.buton.clicked.connect(self.kont)
        self.launch.clicked.connect(self.upa)
        self.view.clicked.connect(self.urr)


            
    def kont(self):
        hak = 0
        while (hak<99):
            num = self.create()
            self.cursor.execute("select numara from lib where numara = ?",(num,))
            data = self.cursor.fetchall()
            if   len(data) == 0 and num.startswith("0551"):
                self.message.setText("numara bulundu:" + num)
                self.cursor.execute("insert into lib values(?)",(num,))
                self.con.commit()
                break
            elif hak == 100:
                return "bulunamadı"
                break
            else:
                hak += 1
    def upa(self):
        numa = self.sorgu.text()
        self.cursor.execute("select numara from lib where numara = ?",(numa,) )
        data = self.cursor.fetchall()
        if len(data) == 0:
            self.message.setText("böyle bir numara yok")
        else:
            self.message.setText("numara bulundu")
    def urr(self):
        tyy = list()
        iha = self.sorgu.text()
        self.cursor.execute("select numara from lib")
        tam = self.cursor.fetchall()
        for b in tam:
            stnum = b[0]
            if stnum.startswith(iha):
                    tyy.append(stnum)
        if tyy:
            self.message.setText("bulunan numaralar:\n" + "\n".join(tyy))
        else:
            self.message.setText("bulunamadı")
                


             
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet("""
        QWidget {
            background-color: #dddddd;
        }

                      
                      
        QLabel {
                        color: #2e5375;
                        font-size: 16px;
                            }
        QPushButton { /* Tüm butonlar için genel stil */
            background-color: #tttttt; /* Mavi */
            color: white;
            font-size: 14px;
            font-weight: bold;
            padding: 10px 15px;
            border: none;
            border-radius: 5px;
            margin: 5px; /* Butonlar arasında boşluk */
        }
        QPushButton:hover {
            background-color: #0056b3; /* Hover rengi */
        }
        QPushButton:pressed {
            background-color: #004085; /* Basılma rengi */
        }
        #queryInput { /* QLineEdit için stil */
                      background-color: #28d193;
            color: #fcfffe; /* Siyahımsı metin rengi */
            font-size: 16px;
            padding: 8px;
            border: 1px solid #cccccc;
            border-radius: 5px;
                      }
        #generateButton { /* "Launch" butonu için özel stil (yeşil) */
            background-color: #28a745;
        }
        #generateButton:hover {
            background-color: #218838;
        }
        #generateButton:pressed {
            background-color: #1e7e34;
        }
        #viewButton { /* "View" butonu için özel stil (mor) */
            background-color: #6f42c1;
        }
        #viewButton:hover {
            background-color: #563d7c;
        }
        #viewButton:pressed {
            background-color: #492e66;
        }
        #messageLabel {
                      background-color: #c1c9c3;
                      color: #000301;
                      font-size: 15px;
                      font-weight: bold;
                      padding: 5px;
                      min-height: 50px;
                      border: 2px solid #ddd;
                      border-radius: 5px;}
                      
        
    """)
    window = mobile()
    window.show()
    # PyQt5'te uygulama döngüsü exec_() ile başlatılır.
    sys.exit(app.exec_())


