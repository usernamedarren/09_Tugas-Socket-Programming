import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
import socket
import threading

# Fungsi terima pesan
def receive_messages(client_socket, chat_area):
    while True:
        try:
            message, _ = client_socket.recvfrom(1024)
            chat_area.config(state=tk.NORMAL)  # Membuat area chat bisa diedit sementara
            chat_area.insert(tk.END, f"\nServer: {message.decode()}\n")  # Tambah pesan dari server
            chat_area.config(state=tk.DISABLED)  # Kunci area chat, tidak bisa diedit
            chat_area.yview(tk.END)  # Scroll otomatis ke chat yang baru
        except Exception as e:
            print(f"Kesalahan saat menerima pesan: {e}")
            break

# Fungsi kirim pesan
def send_message(client_socket, entry_message, chat_area, server_ip, server_port):
    message = entry_message.get()
    if message.strip().lower() == "exit":
        client_socket.close()
        return
    #else:
    client_socket.sendto(message.encode(), (server_ip, server_port))
        #entry_message.delete(0, tk.END)
    # Bubble chat
    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, f"\nYou: {message}\n")
    chat_area.config(state=tk.DISABLED)
    chat_area.yview(tk.END)
    entry_message.delete(0, tk.END)

def on_enter(event, client_socket, entry_message, server_ip, server_port):
    send_message(client_socket, entry_message, server_ip, server_port)
def start_client():
    root = tk.Tk() #Membuat jendela GUI
    root.title("AkuTauDiaTau Private Chat Room")

    # Bagian judul
    top_frame = tk.Frame(root, bg="#128C7E", height=50)
    top_frame.pack(fill=tk.X)

    top_label = tk.Label(top_frame, text="AkuTauDiaTAu", fg="white", bg="#128C7E", font=("Helvetica", 16))
    top_label.pack(pady=10)

    # Area chat (scrollable)
    chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Helvetica", 12), bg="#ECE5DD")
    chat_area.config(state=tk.DISABLED)  # Area chat hanya untuk tampilan
    chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Bagian bawah: tempat untuk input pesan
    bottom_frame = tk.Frame(root, bg="#FFFFFF", height=50)
    bottom_frame.pack(fill=tk.X, side=tk.BOTTOM)

    entry_message = tk.Entry(bottom_frame, font=("Helvetica", 14), width=40)
    entry_message.pack(side=tk.LEFT, padx=10, pady=10)

    button_send = tk.Button(bottom_frame, text="Send", bg="#25D366", fg="white",
                            font=("Helvetica", 14), command=lambda: send_message(client_socket, entry_message, chat_area, server_ip, server_port))
    button_send.pack(side=tk.RIGHT, padx=10, pady=10)
    
    server_ip = "127.0.0.1" #buat socket
    server_port = 12345
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    password = simpledialog.askstring("Password", "Masukkan password untuk bergabung ke chatroom:", show='*')  # Minta Password dari user
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
        root = tk.Tk() #Membuat jendela GUI
        root.title(f"{username} box")
        client_socket.sendto(username.encode(), (server_ip, server_port)) #kirim username
        

        # Kirim pesan ke server
        text_area = tk.Text(root, height=20, width=50)
        text_area.pack(pady=10)
        
        # Input field untuk pesan
        entry_message = tk.Entry(root, width=50)
        entry_message.pack(side=tk.LEFT, padx=10, pady=10)
        entry_message.bind("<Return>", lambda event: on_enter(event, client_socket, entry_message, server_ip, server_port))
        
        # Tombol kirim
        button_send = tk.Button(root, text="Kirim", command=lambda: send_message(client_socket, entry_message, server_ip, server_port))
        button_send.pack(side=tk.RIGHT, padx=10, pady=10)
        while True:
            message = input()
            if message.strip().lower() == "exit":
                break
            client_socket.sendto(message.encode(), (server_ip, server_port))
        
        threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()
        root.mainloop()
    else:
        messagebox.showerror("[ERROR]", "Password salah, koneksi ditolak.")
        client_socket.close()


if __name__ == "__main__":
    start_client()
