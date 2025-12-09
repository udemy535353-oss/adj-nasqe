import os
import shutil
import sqlite3
import sys
from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QHBoxLayout, 
    QLabel, QApplication, QMessageBox, QFileDialog, QListWidget
)
from mutagen.mp3 import MP3
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
import pygame
# Hedef klasörü tanımlıyoruz ve varlığını kontrol ediyoruz (Güvenlik için)
DESTINATION_FOLDER = r"C:\Users\halim\OneDrive\Ekler\Masaüstü\MySQL\music\musics"
if not os.path.exists(DESTINATION_FOLDER):
    os.makedirs(DESTINATION_FOLDER)

# Tablo adını sabitliyoruz
DB_TABLE_NAME = "music_library" 

class MusicApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        pygame.init()
        pygame.mixer.init()
        self.connect_db()
        self.start_ui()
        
    
    # ----------------------------------------------------
    # VERİTABANI İŞLEMLERİ
    # ----------------------------------------------------
    def connect_db(self):
        self.con = sqlite3.connect("music.db")
        self.cursor = self.con.cursor()
        # Tablo adını sabitledik ve tutarlı hale getirdik
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {DB_TABLE_NAME} (music TEXT, gender TEXT)")
        self.con.commit()
        
    # ----------------------------------------------------
    # ARAYÜZ (UI) İŞLEMLERİ
    # ----------------------------------------------------
    def start_ui(self):
       
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setWindowTitle("Music Player")
        
       
        self.button = QPushButton("Müzik Ekle")
        self.stop = QPushButton("stop")
        self.start = QPushButton("start")
        self.list_widget = QListWidget() 

        
        self.list_widget.item
        self.update_list() 
        
      
        self.button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0, 
                    stop: 0.28 #3186FF,
                    stop: 0.4445 #346BF0,
                    stop: 0.9955 #4EA0FF
                );
                padding: 10px 20px; /* Padding artırıldı */
                border: 2px solid white;
                border-radius: 15px; /* Yarıçap uygulandı */
                color: white;
                min-width: 150px; /* Butonun minimum genişliği */
            }
            QPushButton:pressed {
                /* App seviyesindeki :pressed stili kullanılacak, boş bırakıldı */
            }
        """)
        
       
        self.setStyleSheet("""
            MusicApp { /* Sınıf adını kullanın */
                background-color: #3498DB;
                border: 2px solid #2980B9; 
                border-radius: 40px; 
            }
                           QListWidget {
                           border: 2px solid white;

                           
                           border-radius:10px;
                           
                           }
QListWidget::item {
                           
                       border-radius:15px;
                       margin:15px;
                       background-color:#ede9e8; 
                           
                           
                           }
            
QListWidget::item:hover {
                           
                       background-color:#c2c0c0    
                           
                           
                           
                           }                    




        """)
        
        
        v_layout = QVBoxLayout()
        v_layout.addWidget(self.button)
        v_layout.addWidget(self.stop)
        v_layout.addWidget(self.list_widget)
        
        
        h_layout = QHBoxLayout()
        h_layout.addStretch()
        h_layout.addWidget(self.start)
        h_layout.addLayout(v_layout)
        h_layout.addStretch()
        
        self.setLayout(h_layout)
        


                           
                           
                           
        self.button.clicked.connect(self.add_music)
        self.list_widget.itemClicked.connect(self.play_music)
        self.stop.clicked.connect(self.stop_mus)
        self.start.clicked.connect(self.start_mus)

    def update_list(self):
        """Veritabanından müzikleri çekip listeye ekler."""
        self.list_widget.clear()
        listed = self.cursor.execute(f"SELECT music FROM {DB_TABLE_NAME} order by gender DESC")
        for item in self.cursor.fetchall():
            self.list_widget.addItem(item[0])

    # ----------------------------------------------------
    # MÜZİK EKLEME İŞLEMİ
    # ----------------------------------------------------
    def add_music(self):
        file_filter = "Müzik Dosyaları (*.mp3 *.wav *.flac);;Tüm Dosyalar (*.*)"
        
        selected_file, _ = QFileDialog.getOpenFileName(
            self, "Müzik Dosyası Seç", os.path.expanduser("~"), file_filter
        )
        
        if selected_file:
            source_path = selected_file
            file_name = os.path.basename(source_path)
            
            
            destination_path = os.path.join(DESTINATION_FOLDER, file_name) 

            try:
                
                shutil.copy2(source_path, destination_path)
                
                
                self.cursor.execute(f"INSERT INTO {DB_TABLE_NAME} VALUES(?,?)", (file_name, '1'))
                self.con.commit()
                
               
                self.update_list()
                QMessageBox.information(
                    self, "Başarılı", f"'{file_name}' başarıyla eklendi."
                )
            
            except shutil.SameFileError:
                QMessageBox.warning(
                    self, "Uyarı", f"'{file_name}' dosyası zaten arşivde mevcut."
                )
            except Exception as e:
                QMessageBox.critical(
                    self, "Hata", f"Dosya kopyalama hatası: {e}"
                )
    def play_music(self,item):
        music_name = item.text()

        path = r"C:\Users\halim\OneDrive\Ekler\Masaüstü\MySQL\music\musics/"+music_name

        music = pygame.mixer.music.load(path)
        pygame.mixer.music.play()

        print(music_name)
    def stop_mus(self):
        pygame.mixer.music.pause()
    def start_mus(self):
        pygame.mixer.music.unpause()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    
    app.setStyleSheet("""
        QPushButton:pressed {
            background: #FF5733; /* Basıldığında turuncu-kırmızı renk */
            border: 2px solid white;
        }
    """)
    
    music_app = MusicApp()
    music_app.show()
    sys.exit(app.exec_())