import tkinter as tk
from tkinter import simpledialog, messagebox
import socket
import threading

def receive_messages(client_socket, text_area):
    while True:
        try:
            message, _ = client_socket.recvfrom(1024)
            text_area.insert(tk.END, f"\n{message.decode()}")
        except Exception as e:
            print(f"Kesalahan saat menerima pesan: {e}")
            break

def send_message(client_socket, entry_message, server_ip, server_port):
    message = entry_message.get()
    if message.strip().lower() == "exit":
        client_socket.close()
    else:
        client_socket.sendto(message.encode(), (server_ip, server_port))
        entry_message.delete(0, tk.END)


def start_client():
    root = tk.Tk() #Membuat jendela GUI
    root.title("Chat Client")

    server_ip = "127.0.0.1" #buat socket
    server_port = 12345
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    password = simpledialog.askstring("Password", "Masukkan password untuk bergabung ke chatroom:", show='*')  # Kirim password ke server
    if not password:
        messagebox.showerror("Error", "Password tidak boleh kosong!")
        return
    
    client_socket.sendto(password.encode(), (server_ip, server_port)) #kirim pass ke server
    
    # Terima respon password
    response, _ = client_socket.recvfrom(1024)
    if "Password diterima" in response.decode():
        # Masukkan username
        username = simpledialog.askstring("Username", "Masukkan username:")
        if not username:
            messagebox.showerror("Error", "Username tidak boleh kosong!")
            return
        client_socket.sendto(username.encode(), (server_ip, server_port)) #kirim username
        

        # Kirim pesan ke server
        text_area = tk.Text(root, height=20, width=50)
        text_area.pack(pady=10)
        
        # Input field untuk pesan
        entry_message = tk.Entry(root, width=40)
        entry_message.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Tombol kirim
        button_send = tk.Button(root, text="Kirim", command=lambda: send_message(client_socket, entry_message, server_ip, server_port))
        button_send.pack(side=tk.RIGHT, padx=10, pady=10)
        '''while True:
            message = input()
            if message.strip().lower() == "exit":
                break
            client_socket.sendto(message.encode(), (server_ip, server_port))'''
        
        threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()
    else:
        messagebox.showerror("Error", "Password salah, koneksi ditolak.")
        client_socket.close()


if __name__ == "__main__":
    start_client()
