import os
import threading
import http.server
import socketserver
import webbrowser
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
from googlesearch import search
import time

# --- Ayarlar ---
YEREL_KLASOR = "indirilen_site"
YEREL_SUNUCU_PORTU = 8000
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

def google_ile_site_bul(sorgu):
    """
    Verilen sorgu için Google'da arama yapar ve ilk sonucu döndürür.
    """
    print(f"'{sorgu}' için Google'da ilk sonuç aranıyor...")
    try:
        # Google'dan sonuçları çek, sadece ilk sonucu al
        sonuclar = search(sorgu, num_results=1, lang="tr")
        ilk_sonuc = next(sonuclar, None)
        return ilk_sonuc
    except Exception as e:
        print(f"Arama sırasında bir hata oluştu: {e}")
        return None

def siteyi_kopyala(url, klasor):
    """
    Bir web sitesinin kaynaklarını yerel bir klasöre indirir.
    (Bu fonksiyon önceki kodlarımızdan alınmıştır)
    """
    try:
        print(f"'{url}' adresine bağlanılıyor ve site kopyalanıyor...")
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"❌ ANA SAYFA İNDİRİLEMEDİ. Durum Kodu: {response.status_code}")
            return False

        print("✅ Ana sayfa başarıyla indirildi.")
        os.makedirs(klasor, exist_ok=True)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        kaynak_taglari = soup.find_all(['link', 'script', 'img'])
        for tag in kaynak_taglari:
            kaynak_url_niteligi = 'href' if tag.name == 'link' else 'src'
            kaynak_url = tag.get(kaynak_url_niteligi)
            if not kaynak_url: continue
            
            if kaynak_url.startswith('//'): tam_kaynak_url = 'https:' + kaynak_url
            else: tam_kaynak_url = urljoin(url, kaynak_url)
            
            kaynak_path = urlparse(tam_kaynak_url).path.lstrip('/')
            if not kaynak_path: continue
            yerel_dosya_yolu = os.path.join(klasor, kaynak_path)
            
            os.makedirs(os.path.dirname(yerel_dosya_yolu), exist_ok=True)

            try:
                kaynak_response = requests.get(tam_kaynak_url, headers=HEADERS)
                if kaynak_response.status_code == 200:
                    with open(yerel_dosya_yolu, 'wb') as f: f.write(kaynak_response.content)
                    tag[kaynak_url_niteligi] = kaynak_path
            except Exception:
                pass

        with open(os.path.join(klasor, "index.html"), "w", encoding='utf-8') as f:
            f.write(str(soup))
            
        print("\n✅ Site kopyalama tamamlandı!")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Siteye bağlanırken kritik bir hata oluştu: {e}")
        return False

def sunucuyu_baslat(klasor, port):
    """
    Belirtilen klasörde basit bir Python web sunucusu başlatır.
    """
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=klasor, **kwargs)
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"\nSunucu http://localhost:{port} adresinde başlatıldı.")
        print("Tarayıcıda yerel kopya açılıyor...")
        print("Programı tamamen kapatmak için terminalde Ctrl+C'ye basın.")
        httpd.serve_forever()

# --- Ana Program ---
if __name__ == "__main__":
    sorgu = input("Hangi konu hakkında bir site aramak istersin? -> ")
    if not sorgu:
        print("Arama yapmak için bir şey girmediniz.")
    else:
        hedef_url = google_ile_site_bul(sorgu)
        
        if hedef_url:
            print(f"Bulunan site: {hedef_url}")
            if siteyi_kopyala(hedef_url, YEREL_KLASOR):
                # Sunucuyu ve tarayıcıyı başlat
                server_thread = threading.Thread(target=sunucuyu_baslat, args=(YEREL_KLASOR, YEREL_SUNUCU_PORTU))
                server_thread.daemon = True
                server_thread.start()
                time.sleep(1) # Sunucunun başlaması için kısa bir bekleme
                webbrowser.open(f"http://localhost:{YEREL_SUNUCU_PORTU}/index.html")
                
                # Ana programın kapanmaması için bekle
                try:
                    server_thread.join()
                except KeyboardInterrupt:
                    print("\nProgram kapatılıyor.")
        else:
            print("Bu arama için bir site bulunamadı.")