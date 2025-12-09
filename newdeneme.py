
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
import time


DEFAULT_SERVER_HOST = 'localhost'
DEFAULT_SERVER_PORT = 65432


client_socket = None
stop_threads = False 
username = "Kullanıcı" 


window = None
messages_area = None
message_input = None
send_button = None
status_bar = None



def update_status(message):
    """Durum çubuğunu günceller."""
    if status_bar:
        status_bar.config(text=message)

def display_message(message):
    """Mesajları ana metin alanında gösterir."""
    if messages_area:
        messages_area.config(state=tk.NORMAL)
        messages_area.insert(tk.END, message + "\n")
        messages_area.yview(tk.END) 
        messages_area.config(state=tk.DISABLED)

def receive_messages():
    """Sunucudan gelen mesajları dinler ve GUI'de gösterir."""
    global stop_threads
    global client_socket
    while not stop_threads:
        if not client_socket:
            time.sleep(0.1) 
            continue
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                display_message(message)
            else:
                
                display_message("[SİSTEM] Sunucu bağlantıyı kapattı.")
                update_status("Bağlantı kesildi.")
                stop_threads = True
                break
        except ConnectionResetError:
            display_message("[SİSTEM] Sunucu bağlantıyı aniden kapattı.")
            update_status("Bağlantı sıfırlandı.")
            stop_threads = True
            break
        except socket.timeout:  
            continue
        except OSError as e: 
            if not stop_threads: 
                 display_message(f"[SİSTEM] Mesaj alınırken hata oluştu: {e}")
            update_status("Soket hatası.")
            stop_threads = True
            break
        except Exception as e:
            if not stop_threads:
                display_message(f"[SİSTEM] Bir hata oluştu: {e}")
            update_status("Bilinmeyen bir hata oluştu.")
            stop_threads = True
            break
    
    if client_socket:
        try:
            client_socket.close()
        except:
            pass
    client_socket = None 
    if send_button:
        send_button.config(state=tk.DISABLED)
    if message_input:
        message_input.config(state=tk.DISABLED)
    print("Mesaj alma thread'i sonlandırıldı.")


def send_message(event=None): 
    """Kullanıcının girdiği mesajı sunucuya gönderir."""
    global stop_threads
    if stop_threads or not client_socket:
        messagebox.showerror("Hata", "Sunucuya bağlı değilsiniz.")
        return

    message_content = message_input.get()
    if message_content:
        full_message = f"{message_content}" 
        try:
            client_socket.sendall(full_message.encode('utf-8'))
            
            message_input.delete(0, tk.END) 
            if message_content.lower() == 'exit':
                display_message("[SİSTEM] Sohbetten ayrılıyorsunuz...")
                stop_threads = True 
        except socket.error as e:
            display_message(f"[SİSTEM] Mesaj gönderilemedi: {e}")
            update_status("Mesaj gönderilemedi.")
            stop_threads = True 
        except Exception as e:
            display_message(f"[SİSTEM] Mesaj gönderirken hata: {e}")
            update_status("Mesaj gönderme hatası.")
            stop_threads = True

def on_closing():
    """Pencere kapatıldığında yapılacak işlemler."""
    global stop_threads
    global client_socket
    if messagebox.askokcancel("Çıkış", "Uygulamadan çıkmak istediğinize emin misiniz?"):
        stop_threads = True
        if client_socket:
            try:
                
                client_socket.sendall("exit_gui_client".encode('utf-8'))
                client_socket.close()
            except socket.error:
                pass 
            client_socket = None
        
        
        time.sleep(0.2) 
        if window:
            window.destroy()
        print("İstemci uygulaması kapatıldı.")

def connect_to_server():
    """Sunucuya bağlanmayı dener."""
    global client_socket
    global stop_threads
    global username

    
    server_host_addr = simpledialog.askstring("Sunucu Bilgileri", "Sunucu IP Adresi:", initialvalue=DEFAULT_SERVER_HOST)
    if not server_host_addr:
        update_status("Bağlantı iptal edildi.")
        return

    try:
        server_port_addr = simpledialog.askinteger("Sunucu Bilgileri", "Sunucu Port Numarası:", initialvalue=DEFAULT_SERVER_PORT, minvalue=1024, maxvalue=65535)
        if not server_port_addr:
            update_status("Bağlantı iptal edildi.")
            return
    except: 
        messagebox.showerror("Hata", "Geçersiz port numarası.")
        update_status("Geçersiz port.")
        return

    user_name_input = simpledialog.askstring("Kullanıcı Adı", "Kullanıcı adınız:", initialvalue=f"Kullanıcı{int(time.time())%1000}")
    if not user_name_input:
        update_status("Kullanıcı adı girilmedi, varsayılan kullanılıyor.")
    else:
        username = user_name_input


    stop_threads = False 
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(5) 

    try:
        update_status(f"{server_host_addr}:{server_port_addr} adresine bağlanılıyor...")
        client_socket.connect((server_host_addr, server_port_addr))
        client_socket.settimeout(None) 
        
        client_socket.sendall(f"USERNAME:{username}".encode('utf-8'))

        update_status(f"Bağlandı: {server_host_addr}:{server_port_addr} | Kullanıcı: {username}")
        display_message(f"[SİSTEM] Sunucuya bağlandınız. Kullanıcı adınız: {username}")
        
        if send_button:
            send_button.config(state=tk.NORMAL)
        if message_input:
            message_input.config(state=tk.NORMAL)
            message_input.focus_set() 

        # Mesajları almak için thread başlat
        receive_thread = threading.Thread(target=receive_messages, daemon=True)
        receive_thread.start()

    except socket.timeout:
        messagebox.showerror("Bağlantı Hatası", f"Zaman aşımı: {server_host_addr}:{server_port_addr} adresine bağlanılamadı.")
        update_status("Bağlantı zaman aşımı.")
        client_socket = None
    except socket.error as e:
        messagebox.showerror("Bağlantı Hatası", f"Sunucuya bağlanılamadı: {e}")
        update_status(f"Bağlantı hatası: {e}")
        client_socket = None
    except Exception as e:
        messagebox.showerror("Hata", f"Bilinmeyen bir hata oluştu: {e}")
        update_status(f"Bilinmeyen hata: {e}")
        client_socket = None


def main_gui():
    """Ana GUI penceresini oluşturur ve başlatır."""
    global window, messages_area, message_input, send_button, status_bar

    window = tk.Tk()
    window.title(f"Sohbet İstemcisi")

    window_width = 500
    window_height = 400
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)
    window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    window.minsize(300, 250)

    menubar = tk.Menu(window)
    connection_menu = tk.Menu(menubar, tearoff=0)
    connection_menu.add_command(label="Sunucuya Bağlan", command=connect_to_server)
    connection_menu.add_separator()
    connection_menu.add_command(label="Çıkış", command=on_closing)
    menubar.add_cascade(label="Bağlantı", menu=connection_menu)
    window.config(menu=menubar)


    main_frame = tk.Frame(window)
    main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10) 

    

    
    input_frame = tk.Frame(main_frame)
    input_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(5, 0)) 

    message_input = tk.Entry(input_frame, font=("Arial", 11), relief=tk.SOLID, borderwidth=1)
    message_input.pack(side=tk.LEFT, expand=True, fill=tk.X, ipady=5, padx=(0, 5)) 
    message_input.bind("<Return>", send_message)
    message_input.config(state=tk.DISABLED) 

    send_button = tk.Button(input_frame, text="Gönder", command=send_message, font=("Arial", 10, "bold"), relief=tk.RAISED, padx=10)
    send_button.pack(side=tk.RIGHT) # Sağda
    send_button.config(state=tk.DISABLED) 

    
    messages_area = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, state=tk.DISABLED, font=("Arial", 10))
    
    
    messages_area.pack(side=tk.TOP, expand=True, fill=tk.BOTH, pady=(0, 5))

    

    
    status_bar = tk.Label(window, text="Sunucuya bağlı değil.", bd=1, relief=tk.SUNKEN, anchor=tk.W, padx=5, pady=2)
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.after(100, connect_to_server)
    window.mainloop()

if __name__ == "__main__":
    main_gui()
