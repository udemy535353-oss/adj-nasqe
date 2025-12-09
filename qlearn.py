from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QApplication,QHBoxLayout,QFileDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt,QSize
from PyQt5.QtGui import QPixmap,QImage
import sys
import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
DİRECTOR = r"C:\recycle"
os.chdir(DİRECTOR)
class QLearnWidget(QtWidgets.QWidget):
    def __init__(self):
        self.file_path= "C:/recycle/gray_image.png"
        super().__init__()
        
        self.initUI()
    def initUI(self):
        self.setWindowTitle('Q-Learning Configuration')
        
        
        h = QHBoxLayout()
        vbox = QVBoxLayout()


        self.müsti = QLabel("Mustafa bana inanmıyor")
        self.müsti.setAlignment(Qt.AlignCenter)
        vbox.addWidget(self.müsti)

        
        self.resim_label = QLabel("Buraya Resim Gelecek")
        self.resim_label.setAlignment(Qt.AlignCenter)
        self.resim_label.setStyleSheet("border: 1px solid gray;")
        SABIT_BOYUT = QSize(1000,800) 
        self.resim_label.setFixedSize(SABIT_BOYUT)
        
        
        self.resim_label.setScaledContents(True)
        vbox.addWidget(self.resim_label)

        
        self.sec_buton = QPushButton("Resim Seç...")
        self.sec_buton.clicked.connect(self.resim_sec)
        vbox.addWidget(self.sec_buton)
        self.alpha = QLineEdit()
        self.alpha.setPlaceholderText("Alpha Değerini Girin")
        self.alpha.setFixedWidth(200)
        self.but = QPushButton("Hesapla")
        self.but.clicked.connect(self.calc)
        self.hopper = QPushButton("Orijinal Resim")
        self.hopper.clicked.connect(self.sta)
        self.showw = QPushButton("Göster")
        self.showw.clicked.connect(self.qt_show)
        h.addWidget(self.showw)


        h.addWidget(self.but)
        h.addWidget(self.hopper)
        h.addWidget(self.alpha)
        h.addStretch()
        vbox.addLayout(h)
        
        
        
        
        self.setLayout(vbox)
        self.show()
    def resim_sec(self):
        self.dosya_yolu, _ = QFileDialog.getOpenFileName(
            self,                                         
            "Resim Dosyası Seç",
            "",                                            
            "Resim Dosyaları (*.png *.jpg *.jpeg *.bmp)"
        )

        print(self.dosya_yolu)
        
        if self.dosya_yolu:
            pixmap = QPixmap(self.dosya_yolu)

            
            



            self.resim_label.setPixmap(pixmap)
    def calc(self):
        with open(self.dosya_yolu, 'rb') as f:
            bytes_data = f.read()


        img_array = np.frombuffer(bytes_data, np.uint8)
        img = cv2.imdecode(img_array,cv2.IMREAD_COLOR)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        cv2.imwrite("gray_image.png", img_gray)
        
        pixmap = QPixmap(self.file_path)
        self.resim_label.setPixmap(pixmap)
    def sta(self):
        with open(self.dosya_yolu, 'rb') as f:
            bytes_data = f.read()
        img_array = np.frombuffer(bytes_data, np.uint8)
        img = cv2.imdecode(img_array,cv2.IMREAD_COLOR)
        cv2.imwrite("gray_image.png", img)
        pixmap = QPixmap(self.dosya_yolu)
        self.resim_label.setPixmap(pixmap)
    def qt_show(self):
        img_forshow = cv2.imread(self.file_path)
        img_forshow=cv2.cvtColor(img_forshow, cv2.COLOR_BGR2RGB)
        plt.imshow(img_forshow)
        plt.title("IMAGE")
        
        plt.axis('off') 
        plt.show()
        
        
    
    
        
        



            

        

                
            
            

app = QApplication(sys.argv)
widget = QLearnWidget()
sys.exit(app.exec_())




