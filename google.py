import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import defaultdict
import time

class SimpleSearchEngine:
    def __init__(self, base_url="http://wikipedia.com"):
        self.base_url = base_url
        # İndeks: {kelime: {url1: frekans1, url2: frekans2, ...}}
        self.index = defaultdict(lambda: defaultdict(int))
        self.visited_urls = set()
        self.to_visit = [self.base_url]
        self.max_pages_to_crawl = 50 # Tarama yapacağımız maksimum sayfa sayısı

    def is_valid_url(self, url):
        """URL'nin geçerli olup olmadığını ve temel URL ile aynı domain'de olup olmadığını kontrol eder."""
        parsed_url = urlparse(url)
        return bool(parsed_url.netloc) and bool(parsed_url.scheme) and parsed_url.netloc.endswith(urlparse(self.base_url).netloc)

    def crawl(self):
        """Web sayfalarını tarar ve indeksler."""
        print(f"Taramaya başlanıyor: {self.base_url}")
        
        while self.to_visit and len(self.visited_urls) < self.max_pages_to_crawl:
            current_url = self.to_visit.pop(0)
            
            if current_url in self.visited_urls:
                continue

            self.visited_urls.add(current_url)
            print(f"Taranıyor: {current_url}")

            try:
                response = requests.get(current_url, timeout=5)
                response.raise_for_status() # HTTP hataları için istisna fırlatır
                soup = BeautifulSoup(response.text, 'html.parser')

                # Sayfa içeriğini al ve kelimeleri işle
                text = soup.get_text().lower()
                words = text.split() # Basit kelime ayırma

                for word in words:
                    # Noktalama işaretlerini temizleyelim (basit bir yaklaşım)
                    cleaned_word = ''.join(filter(str.isalnum, word))
                    if cleaned_word:
                        self.index[cleaned_word][current_url] += 1
                
                # Bağlantıları bul ve ziyaret edilecekler listesine ekle
                for link in soup.find_all('a', href=True):
                    absolute_url = urljoin(current_url, link['href'])
                    if self.is_valid_url(absolute_url) and absolute_url not in self.visited_urls:
                        self.to_visit.append(absolute_url)
                        
            except requests.exceptions.RequestException as e:
                print(f"Hata oluştu {current_url}: {e}")
            except Exception as e:
                print(f"Beklenmedik bir hata oluştu {current_url}: {e}")
            
            time.sleep(0.1) # Sunucuyu yormamak için küçük bir gecikme

        print(f"\nTaramalar tamamlandı. Toplam {len(self.visited_urls)} sayfa ziyaret edildi.")
        print(f"İndekste {len(self.index)} benzersiz kelime bulundu.")

    def search(self, query):
        """Verilen sorguya göre sonuçları döndürür."""
        query_words = query.lower().split()
        results = defaultdict(int) # URL ve puanı tutacak

        if not query_words:
            return {}

        # Her kelime için sonuçları birleştir ve puanla
        for word in query_words:
            cleaned_word = ''.join(filter(str.isalnum, word))
            if cleaned_word in self.index:
                for url, freq in self.index[cleaned_word].items():
                    # Basit puanlama: Kelimenin geçtiği sayfa sayısı ve kelimenin sıklığına göre
                    results[url] += freq 
        
        # Sonuçları puanlarına göre sırala (en yüksek puan ilk)
        sorted_results = sorted(results.items(), key=lambda item: item[1], reverse=True)
        
        return dict(sorted_results)

# --- Kullanım Örneği ---
if __name__ == "__main__":
    # DİKKAT: Gerçek bir siteyi tararken sunucuya yük bindirmemek için 
    # 'max_pages_to_crawl' değerini düşük tutun ve test için 
    # kendi yerel sunucunuzu veya izin verilen siteleri kullanın.
    # example.com genellikle test için kullanılır.
    
    search_engine = SimpleSearchEngine(base_url="http://example.com") 
    
    # Taramayı başlat
    search_engine.crawl()

    print("\n--- Arama Örneği ---")
    user_query = input("Arama sorgunuzu girin: ")
    
    search_results = search_engine.search(user_query)
    
    if search_results:
        print(f"\n'{user_query}' için bulunan sonuçlar:")
        for url, score in search_results.items():
            print(f"- {url} (Puan: {score})")
    else:
        print(f"'{user_query}' için sonuç bulunamadı.")

    # İndeksin bir kısmını görmek isterseniz:
    # print("\n--- İndeks Örneği (İlk 5 Kelime) ---")
    # count = 0
    # for word, urls in search_engine.index.items():
    #     if count < 5:
    #         print(f"'{word}': {dict(urls)}")
    #         count += 1
    #     else:
    #         break