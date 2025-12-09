import sys
import os

from PyQt5.QtWidgets import QWidget,QApplication,QTextEdit,QLabel,QPushButton,QVBoxLayout,QFileDialog,QHBoxLayout
from PyQt5.QtWidgets import QAction,qApp,QMainWindow,QMessageBox

class Notepad(QWidget):
    def __init__(self):

        super().__init__()

        self.init_ui()
    def init_ui(self):

        self.yazi_alani = QTextEdit()


        self.temizle = QPushButton("Temizle")
        self.ac = QPushButton("Aç")
        self.kaydet = QPushButton("Kaydet")

        h_box = QHBoxLayout()

        h_box.addWidget(self.temizle)
        h_box.addWidget(self.ac)
        h_box.addWidget(self.kaydet)

        v_box = QVBoxLayout()

        v_box.addWidget(self.yazi_alani)

        v_box.addLayout(h_box)

        self.setLayout(v_box)

        self.setWindowTitle("NotePad")
        self.temizle.clicked.connect(self.yaziyi_temizle)
        self.ac.clicked.connect(self.dosya_ac)
        self.kaydet.clicked.connect(self.dosya_kaydet)

    def yaziyi_temizle(self):
        self.yazi_alani.clear()

    def dosya_ac(self):

        dosya_yolu, _ = QFileDialog.getOpenFileName(self, "Dosya Aç", os.getenv("HOME"), "Metin Dosyaları (*.txt);;Tüm Dosyalar (*.*)")

        if dosya_yolu:
            try:
                with open(dosya_yolu, "r", encoding='utf-8') as file:
                    self.yazi_alani.setText(file.read())
            except Exception as e:
                print(f"HATA: Dosya okunamadı. Sebep: {e}")
                QMessageBox.critical("Warning","we have a problem : {}".format(e))


    def dosya_kaydet(self):
        dosya = QFileDialog.getSaveFileName(self,"Dosya kaydet",os.getenv("HOME"),"Text Files (*.txt);;all files (*)")
        
    
        try:
            
            with open(dosya[0],"w") as rot:
                rot.write(self.yazi_alani.toPlainText())
        except Exception as e:
            QMessageBox.critical("Warning","we have a problem : {} ".format(e))

            
        
            



class Menu(QMainWindow):

    def __init__(self):

        super().__init__()


        self.pencere = Notepad()

        self.setCentralWidget(self.pencere)


        self.menuleri_olustur()
    def menuleri_olustur(self):

        menubar = self.menuBar()

        dosya = menubar.addMenu("Dosya")
        dosya_ac = QAction("Dosya Aç",self)
        dosya_ac.setShortcut("Ctrl+O")
        dosya_kaydet = QAction("Dosya kaydet",self)
        dosya_kaydet.setShortcut("Ctrl+S")
        cıkış = QAction("Çıkış",self)
        cıkış.setShortcut("Ctrl+R")
        self.setWindowTitle("metin editörü")
        dosya.addAction(dosya_ac)
        dosya.addAction(dosya_kaydet)
        dosya.addAction(cıkış)
        self.show()
        dosya.triggered.connect(self.response)
    def response(self,action):
        if action.text() == "Dosya Aç":
            self.pencere.dosya_ac()
        elif action.text() == "Dosya kaydet":
            self.pencere.dosya_kaydet()
        elif action.text() == "Çıkış":
            qApp.quit()

        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("""
QTextEdit {
                      background-color: #b7b2bf;
                      font-weight: bold;
                      font-family: "inter";
                      padding: 8px;
                      border: 4px solid #000000;
                      border-radius: 5px;
                      }

                      
                      
                      
                      
                      
                      
                      
                      
                      
                      """)







    pencere = Menu()
    pencere.show()
    sys.exit(app.exec_())