import tkinter as tk
from tkinter import filedialog, ttk
import pygame
import os

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Basit Müzik Çalar")
        self.root.geometry("400x200")

        # Pygame mixer'ı başlat
        pygame.mixer.init()

        self.current_song_path = ""
        self.is_paused = False

        # --- Arayüz Elemanları ---

        # Stil oluştur
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 12), padding=10)
        style.configure("TLabel", font=("Helvetica", 11), padding=5)

        # Şarkı adı için etiket
        self.song_label = ttk.Label(root, text="Lütfen bir müzik dosyası seçin.", wraplength=380)
        self.song_label.pack(pady=10)

        # Kontrol butonları için bir çerçeve (frame)
        controls_frame = tk.Frame(root)
        controls_frame.pack(pady=20)

        # Butonlar
        self.select_button = ttk.Button(controls_frame, text="🎶 Müzik Seç", command=self.select_song)
        self.select_button.grid(row=0, column=0, padx=5)

        self.play_button = ttk.Button(controls_frame, text="▶️ Oynat", command=self.play_song)
        self.play_button.grid(row=0, column=1, padx=5)
        
        self.pause_button = ttk.Button(controls_frame, text="⏸️ Duraklat", command=self.pause_song)
        self.pause_button.grid(row=0, column=2, padx=5)

        self.stop_button = ttk.Button(controls_frame, text="⏹️ Durdur", command=self.stop_song)
        self.stop_button.grid(row=0, column=3, padx=5)

    def select_song(self):
        """Bilgisayardan bir müzik dosyası seçmek için pencere açar."""
        song_path = filedialog.askopenfilename(
            title="Bir Müzik Dosyası Seçin",
            filetypes=(("MP3 Dosyaları", "*.mp3"), ("WAV Dosyaları", "*.wav"), ("Tüm Dosyalar", "*.*"))
        )
        if song_path:
            self.current_song_path = song_path
            song_name = os.path.basename(song_path) # Dosya yolundan sadece adını al
            self.song_label.config(text=f"Çalınıyor: {song_name}")
            self.play_song() # Seçildikten sonra direkt çal

    def play_song(self):
        """Seçilen şarkıyı oynatır."""
        if not self.current_song_path:
            # Henüz şarkı seçilmediyse bir uyarı ver (isteğe bağlı)
            print("Lütfen önce bir şarkı seçin.")
            return

        if self.is_paused:
            # Eğer duraklatıldıysa devam et
            pygame.mixer.music.unpause()
            self.is_paused = False
        else:
            # Yeni şarkıyı yükle ve oynat
            pygame.mixer.music.load(self.current_song_path)
            pygame.mixer.music.play()

    def pause_song(self):
        """Müziği duraklatır."""
        if pygame.mixer.music.get_busy(): # Sadece müzik çalıyorsa duraklat
            pygame.mixer.music.pause()
            self.is_paused = True

    def stop_song(self):
        """Müziği tamamen durdurur."""
        pygame.mixer.music.stop()
        self.song_label.config(text="Lütfen bir müzik dosyası seçin.")
        self.current_song_path = ""
        self.is_paused = False

# Ana uygulamayı başlat
if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()
    