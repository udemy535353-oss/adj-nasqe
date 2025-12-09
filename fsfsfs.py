import re

class InvertedIndex:
    def __init__(self):
        # Kelimeleri belge kimliklerine eşleyen ana dizin.
        # Format: { "kelime": { belge_id: [konum1, konum2, ...], ... }, ... }
        self.index = {}
        # Belge kimliklerini belge içeriğine eşleyen (isteğe bağlı, debugging için)
        self.documents = {}
        self.next_doc_id = 0 # Otomatik belge kimliği atamak için

    def add_document(self, text):
        """
        Yeni bir belgeyi ters dizine ekler.
        """
        doc_id = self.next_doc_id
        self.documents[doc_id] = text # Belge içeriğini sakla (isteğe bağlı)
        self.next_doc_id += 1

        # Metni kelimelere ayır, küçük harfe dönüştür ve noktalama işaretlerini kaldır
        words = re.findall(r'\b\w+\b', text.lower())

        for position, word in enumerate(words):
            if word not in self.index:
                self.index[word] = {}
            if doc_id not in self.index[word]:
                self.index[word][doc_id] = []
            self.index[word][doc_id].append(position) # Kelimenin konumunu da sakla

        return doc_id

    def search(self, query):
        """
        Ters dizinde bir sorguyu arar ve eşleşen belgelerin kimliklerini döndürür.
        Basit bir AND araması yapar (tüm kelimelerin geçtiği belgeler).
        """
        query_words = re.findall(r'\b\w+\b', query.lower())
        
        if not query_words:
            return []

        # İlk kelimenin geçtiği belgelerle başla
        # Eğer ilk kelime dizinde yoksa, hiç sonuç olmaz.
        first_word_docs = self.index.get(query_words[0], {})
        
        # Sadece belge kimliklerini al
        matching_doc_ids = set(first_word_docs.keys())

        # Diğer tüm kelimeler için kesişim kümesini bul
        for word in query_words[1:]:
            if word not in self.index:
                return [] # Kelimelerden biri bile yoksa, sonuç yok
            matching_doc_ids.intersection_update(self.index[word].keys())

        # Sorgudaki tüm kelimelerin geçtiği belge kimliklerini döndür
        return list(matching_doc_ids)

    def display_index(self):
        """
        Ters dizinin içeriğini görüntüler (debugging için).
        """
        print("--- Ters Dizin ---")
        for word, doc_info in self.index.items():
            print(f"'{word}':")
            for doc_id, positions in doc_info.items():
                print(f"  Belge ID {doc_id}: Konumlar: {positions}")
        print("------------------")

    def get_document_content(self, doc_id):
        """
        Belge kimliğine göre belge içeriğini döndürür.
        """
        return self.documents.get(doc_id)

# --- Kullanım Örneği ---
if __name__ == "__main__":
    inverted_index = InvertedIndex()

    # Belgelerimizi ekleyelim
    doc1_id = inverted_index.add_document("Python programlama dili çok popülerdir ve veri bilimi için kullanılır.")
    doc2_id = inverted_index.add_document("Veri bilimi ve makine öğrenimi Python ile yapılabilir.")
    doc3_id = inverted_index.add_document("Web scraping için Python kütüphaneleri harikadır.")
    doc4_id = inverted_index.add_document("Kütüphaneler, kodun tekrar kullanılabilirliğini artırır.")

    print(f"Belge 1 ID: {doc1_id}")
    print(f"Belge 2 ID: {doc2_id}")
    print(f"Belge 3 ID: {doc3_id}")
    print(f"Belge 4 ID: {doc4_id}\n")

    # Ters dizini görüntüleyelim
    inverted_index.display_index()
    print("\n")

    # Arama yapalım
    query1 = "python programlama"
    results1 = inverted_index.search(query1)
    print(f"'{query1}' için sonuçlar (Belge ID'leri): {results1}")
    if results1:
        print("Eşleşen Belgelerin İçeriği:")
        for doc_id in results1:
            print(f"  Belge ID {doc_id}: {inverted_index.get_document_content(doc_id)}")
    print("\n")

    query2 = "veri bilimi"
    results2 = inverted_index.search(query2)
    print(f"'{query2}' için sonuçlar (Belge ID'leri): {results2}")
    if results2:
        print("Eşleşen Belgelerin İçeriği:")
        for doc_id in results2:
            print(f"  Belge ID {doc_id}: {inverted_index.get_document_content(doc_id)}")
    print("\n")

    query3 = "kütüphaneler artırır"
    results3 = inverted_index.search(query3)
    print(f"'{query3}' için sonuçlar (Belge ID'leri): {results3}")
    if results3:
        print("Eşleşen Belgelerin İçeriği:")
        for doc_id in results3:
            print(f"  Belge ID {doc_id}: {inverted_index.get_document_content(doc_id)}")
    print("\n")

    query4 = "olmayan kelime"
    results4 = inverted_index.search(query4)
    print(f"'{query4}' için sonuçlar (Belge ID'leri): {results4}")