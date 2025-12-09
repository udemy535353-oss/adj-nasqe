
import socket
import threading
import miniupnpc 


HOST = '0.0.0.0'
PORT = 65432       
MAX_CLIENTS = 10
BUFFER_SIZE = 1024
UPNP_DESCRIPTION = "Python Chat Server" 


clients = {}
client_threads = []
lock = threading.Lock()
upnp = None 
external_ip = None 


def setup_port_forwarding_upnp(port_to_forward):
    """UPnP kullanarak port yönlendirmesi yapmayı dener."""
    global upnp
    global external_ip
    print("[UPnP] Port yönlendirmesi deneniyor...")
    try:
        upnp = miniupnpc.UPnP()
        upnp.discoverdelay = 200 
        print(f"[UPnP] {upnp.discover()} UPnP cihaz(lar)ı keşfedildi.")
        
        upnp.selectigd() 
        external_ip = upnp.externalipaddress()
        print(f"[UPnP] Dış IP adresiniz: {external_ip}")

        
        mapping_exists = upnp.getspecificportmapping(port_to_forward, 'TCP')
        if mapping_exists:
            print(f"[UPnP] Port {port_to_forward} (TCP) zaten yönlendirilmiş görünüyor: {mapping_exists}")
                    

        internal_ip = socket.gethostbyname(socket.gethostname()) 

        print(f"[UPnP] Yerel IP (tahmini): {internal_ip}, IGD LAN adresi: {upnp.lanaddr}")

        
        result = upnp.addportmapping(port_to_forward, 'TCP', upnp.lanaddr, port_to_forward, UPNP_DESCRIPTION, '')
        
        if result:
            print(f"[UPnP] BAŞARILI: Port {port_to_forward} (TCP) -> {upnp.lanaddr}:{port_to_forward} adresine yönlendirildi.")
            print(f"[UPnP] Arkadaşlarınızın bağlanması için potansiyel adres: {external_ip}:{port_to_forward}")
            return True
        else:
            print(f"[UPnP] BAŞARISIZ: Port {port_to_forward} (TCP) yönlendirilemedi.")
            return False

    except Exception as e:
        print(f"[UPnP HATA] Port yönlendirme sırasında bir hata oluştu: {e}")
        upnp = None 
        return False

def remove_port_forwarding_upnp(port_to_remove):
    """UPnP ile yapılan port yönlendirmesini kaldırmayı dener."""
    global upnp
    if upnp:
        print(f"[UPnP] Port {port_to_remove} (TCP) için yönlendirme kaldırılıyor...")
        try:
            result = upnp.deleteportmapping(port_to_remove, 'TCP')
            if result:
                print(f"[UPnP] BAŞARILI: Port {port_to_remove} (TCP) yönlendirmesi kaldırıldı.")
            else:
                print(f"[UPnP] BAŞARISIZ: Port {port_to_remove} (TCP) yönlendirmesi kaldırılamadı (belki zaten yoktu).")
        except Exception as e:
            print(f"[UPnP HATA] Port yönlendirmesi kaldırılırken bir hata oluştu: {e}")
    else:
        print("[UPnP] Kaldırılacak aktif bir UPnP yönlendirmesi bulunamadı.")


def broadcast_message(message, sender_socket=None, is_system_message=False):
    with lock:
        if sender_socket and not is_system_message:
            sender_username = clients.get(sender_socket, "Bilinmeyen Kullanıcı")
            full_message = f"{sender_username}: {message}"
        else:
            full_message = message
        
        current_clients = list(clients.keys())
        for client_sock in current_clients:
            if client_sock != sender_socket or is_system_message:
                try:
                    client_sock.sendall(full_message.encode('utf-8'))
                except socket.error:
                    print(f"İstemciye mesaj gönderilemedi: {clients.get(client_sock, client_sock.getpeername())}")
                    remove_client(client_sock)

def remove_client(client_socket):
    with lock:
        if client_socket in clients:
            username = clients.pop(client_socket)
            print(f"İstemci ayrıldı: {username} ({client_socket.getpeername()}). Kalan istemciler: {len(clients)}")
            broadcast_message(f"[SİSTEM] {username} sohbetten ayrıldı.", is_system_message=True)
            try:
                client_socket.close()
            except:
                pass

def handle_client(client_socket, client_address):
    print(f"[YENİ BAĞLANTI] {client_address} bağlandı.")
    username = f"Kullanıcı-{client_address[1]}"
    try:
        initial_message = client_socket.recv(BUFFER_SIZE).decode('utf-8')
        if initial_message.startswith("USERNAME:"):
            username = initial_message.split(":", 1)[1].strip()
            if not username:
                 username = f"Kullanıcı-{client_address[1]}"
        
        with lock:
            clients[client_socket] = username

        client_socket.sendall(f"[SİSTEM] Sohbete hoş geldin, {username}!".encode('utf-8'))
        broadcast_message(f"[SİSTEM] {username} sohbete katıldı.", sender_socket=client_socket, is_system_message=True)

        while True:
            message = client_socket.recv(BUFFER_SIZE).decode('utf-8')
            if not message or message.lower() == "exit_gui_client":
                print(f"[{username} - {client_address}] bağlantıyı kapattı.")
                break
            print(f"[{username} - {client_address}] {message}")
            broadcast_message(message, client_socket)
    except ConnectionResetError:
        print(f"[BAĞLANTI SIFIRLANDI] {username} ({client_address}) bağlantıyı aniden kapattı.")
    except socket.timeout:
        print(f"[ZAMAN AŞIMI] {username} ({client_address}) zaman aşımına uğradı.")
    except Exception as e:
        print(f"[HATA] {username} ({client_address}) ile iletişimde hata: {e}")
    finally:
        remove_client(client_socket)

def start_server():
    global external_ip

    upnp_success = setup_port_forwarding_upnp(PORT)

    if not upnp_success:
        print("-" * 50)
        print("[UYARI] UPnP ile otomatik port yönlendirme BAŞARISIZ oldu.")
        print("Sunucunuz muhtemelen sadece yerel ağınızdan erişilebilir olacaktır.")
        print("Farklı ağlardan erişim için modeminizden manuel port yönlendirme yapmanız gerekebilir:")
        print(f"  Dış Port: {PORT} (TCP) -> İç IP: [Sunucunuzun Yerel IP'si], İç Port: {PORT}")
        print("Genel IP adresinizi öğrenmek için Google'a 'what is my IP' yazabilirsiniz.")
        print("-" * 50)
    else:
        print("-" * 50)
        print("[BİLGİ] UPnP ile port yönlendirme BAŞARILI görünüyor.")
        if external_ip:
            print(f"Arkadaşlarınızın bağlanmak için kullanabileceği adres: {external_ip}:{PORT}")
        else:
            print("Dış IP adresi alınamadı, ancak port yönlendirilmiş olabilir.")
        print("Bu adresin çalışmaması durumunda, genel IP adresinizi manuel olarak kontrol edin.")
        print("-" * 50)


    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((HOST, PORT))
    except socket.error as e:
        print(f"Sunucu başlatılamadı (bind hatası): {e}")
        remove_port_forwarding_upnp(PORT) 
        return

    server_socket.listen(MAX_CLIENTS)
    print(f"[DİNLENİYOR] Sunucu {HOST}:{PORT} adresinde dinlemede...")

    try:
        while True:
            try:
                client_socket, client_address = server_socket.accept()
            except socket.error:
                print("[KAPATILIYOR] Sunucu soketi kapatıldı.")
                break
            except KeyboardInterrupt:
                print("[KAPATILIYOR] Sunucu kapatılıyor (accept sırasında)...")
                break
            
            thread = threading.Thread(target=handle_client, args=(client_socket, client_address), daemon=True)
            thread.start()
            client_threads.append(thread)
                
    except KeyboardInterrupt:
        print("[KAPATILIYOR] Sunucu kapatılıyor...")
    finally:
        print("Tüm istemci bağlantıları kapatılıyor...")
        with lock:
            active_clients_sockets = list(clients.keys())
            for client_sock in active_clients_sockets:
                try:
                    client_sock.sendall("[SİSTEM] Sunucu kapatılıyor. Bağlantınız kesilecek.".encode('utf-8'))
                    remove_client(client_sock)
                except socket.error:
                    pass 
        
        server_socket.close()
        
        remove_port_forwarding_upnp(PORT)
        print("Sunucu başarıyla kapatıldı.")

if __name__ == "__main__":
    start_server()
