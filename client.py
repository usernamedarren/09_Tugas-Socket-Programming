import tkinter as tk
from tkinter import simpledialog, messagebox
import socket
import threading

def create_message_bubble(chat_area, username, message, align_right=False):
    username_label = tk.Label(
        chat_area,
        text=username,
        bg="#DCF8C6" if align_right else "#ECE5DD",
        font=("Helvetica", 12, "bold"),
        padx=10,
        pady=2
    )
    message_label = tk.Label(
        chat_area,
        text=message,
        bg="#DCF8C6" if align_right else "#ECE5DD",
        wraplength=250,
        justify='right' if align_right else 'left',
        anchor='e' if align_right else 'w',
        font=("Helvetica", 12),
        padx=10,
        pady=5
    )
    chat_area.config(state=tk.NORMAL)
    chat_area.window_create(tk.END, window=username_label)
    chat_area.insert(tk.END, '\n')
    chat_area.window_create(tk.END, window=message_label)
    chat_area.insert(tk.END, '\n')
    chat_area.config(state=tk.DISABLED)
    chat_area.yview(tk.END)

def receive_messages(client_socket, chat_area):
    while True:
        try:
            message, _ = client_socket.recvfrom(1024)
            decoded_message = message.decode()

            if "has joined the chatroom" in decoded_message:
                chat_area.config(state=tk.NORMAL)
                chat_area.insert(tk.END, f"\n{decoded_message}\n")
                chat_area.config(state=tk.DISABLED)
            else:
                username_message = decoded_message.split(': ', 1)
                if len(username_message) == 2:
                    username, user_message = username_message
                    create_message_bubble(chat_area, username, user_message, align_right=True)
                else:
                    chat_area.config(state=tk.NORMAL)
                    chat_area.insert(tk.END, f"\n{decoded_message}\n")
                    chat_area.config(state=tk.DISABLED)

        except Exception as e:
            print(f"Error receiving message: {e}")
            break

def on_enter(event, client_socket, entry_message, chat_area, server_ip, server_port):
    send_message(client_socket, entry_message, chat_area, server_ip, server_port)

def send_message(client_socket, entry_message, chat_area, server_ip, server_port):
    message = entry_message.get()
    if message.strip().lower() == "exit":
        client_socket.close()
        return
    if message.strip():
        client_socket.sendto(message.encode(), (server_ip, server_port))
        create_message_bubble(chat_area, "You", message, align_right=False)
        entry_message.delete(0, tk.END)

def start_client():
    root = tk.Tk()
    root.title("Private Chat Room")

    top_frame = tk.Frame(root, bg="#128C7E", height=50)
    top_frame.pack(fill=tk.X)

    top_label = tk.Label(top_frame, text="Chat Room", fg="white", bg="#128C7E", font=("Helvetica", 16))
    top_label.pack(pady=10)

    chat_area = tk.Text(root, wrap=tk.WORD, font=("Helvetica", 12), bg="#ECE5DD")
    chat_area.config(state=tk.DISABLED)
    chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    bottom_frame = tk.Frame(root, bg="#FFFFFF", height=50)
    bottom_frame.pack(fill=tk.X, side=tk.BOTTOM)

    entry_message = tk.Entry(bottom_frame, font=("Helvetica", 14), width=40)
    entry_message.pack(side=tk.LEFT, padx=10, pady=10)

    button_send = tk.Button(bottom_frame, text="Send", bg="#25D366", fg="white",
                            font=("Helvetica", 14), command=lambda: send_message(client_socket, entry_message, chat_area, server_ip, server_port))
    button_send.pack(side=tk.RIGHT, padx=10, pady=10)

    # Bind Enter key to the button as well as the entry_message field
    entry_message.bind("<Return>", lambda event: on_enter(event, client_socket, entry_message, chat_area, server_ip, server_port))
    button_send.bind("<Return>", lambda event: on_enter(event, client_socket, entry_message, chat_area, server_ip, server_port))

    server_ip = simpledialog.askstring("Server IP", "Enter the server IP address:")
    server_port = int(simpledialog.askstring("Server Port", "Enter the server port:"))
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    password = simpledialog.askstring("Password", "Enter password to join the chatroom:", show='*')
    if not password:
        messagebox.showerror("Error", "Password is required!")
        return

    client_socket.sendto(password.encode(), (server_ip, server_port))
    response, _ = client_socket.recvfrom(1024)
    if "Password accepted" in response.decode():
        while True:
            username = simpledialog.askstring("Username", "Enter your username:")
            if not username:
                messagebox.showerror("Error", "Username cannot be empty!")
                continue

            # Send the proposed username to the server for validation
            client_socket.sendto(username.encode(), (server_ip, server_port))
            response, _ = client_socket.recvfrom(1024)
            if "Username accepted" in response.decode():
                break
            else:
                messagebox.showerror("Error", response.decode())

        threading.Thread(target=receive_messages, args=(client_socket, chat_area), daemon=True).start()
        root.mainloop()
    else:
        messagebox.showerror("Error", "Incorrect password, connection denied.")
        client_socket.close()

if __name__ == "__main__":
    start_client()
