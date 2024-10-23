import socket
import threading
import tkinter as tk
from tkinter import messagebox

# Global variables
clients = {}
server_password = ""
server_socket = None
server_thread = None
is_server_running = False

def handle_client():
    global server_socket
    while is_server_running:
        try:
            message, client_address = server_socket.recvfrom(1024)
            decoded_message = message.decode()

            if client_address in clients:
                # Broadcast message to all clients except sender
                for client in clients:
                    if client != client_address:
                        server_socket.sendto(f"{clients[client_address]}: {decoded_message}".encode(), client)
                update_chat_area(f"Message from {clients[client_address]}: {decoded_message}")
            else:
                # First message must be the password, otherwise ignore the client
                if decoded_message == server_password:
                    server_socket.sendto("Password accepted!".encode(), client_address)

                    while True:
                        username, _ = server_socket.recvfrom(1024)
                        username = username.decode().strip()

                        # Check if username is already taken
                        if username in clients.values():
                            server_socket.sendto("Username already taken, please choose a different one.".encode(), client_address)
                        else:
                            # Save client to the dict if username is unique
                            clients[client_address] = username
                            server_socket.sendto("Username accepted".encode(), client_address)
                            update_chat_area(f"New client connected: {username} ({client_address})")

                            # Notify all clients about the new client
                            broadcast_message = f"{username} has joined the chatroom."
                            for client in clients:
                                if client != client_address:
                                    server_socket.sendto(broadcast_message.encode(), client)
                            break
                else:
                    server_socket.sendto("Incorrect password, connection denied.".encode(), client_address)

        except Exception as e:
            update_chat_area(f"Server error: {e}")

def update_chat_area(message):
    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, f"\n{message}\n")
    chat_area.config(state=tk.DISABLED)
    chat_area.yview(tk.END)

def start_server_thread(ip, port, password):
    global server_password, server_socket, server_thread, is_server_running
    server_password = password

    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((ip, int(port)))

    update_chat_area(f"UDP server started on {ip}:{port}")
    is_server_running = True

    # Start the server thread to handle clients
    server_thread = threading.Thread(target=handle_client, daemon=True)
    server_thread.start()

def stop_server():
    global is_server_running, server_socket
    is_server_running = False

    if server_socket:
        server_socket.close()
        update_chat_area("Server stopped.")
    
    # Enable the start button and change colors back
    button_start.config(state=tk.NORMAL, bg="#25D366", text="Start Server")
    button_stop.config(state=tk.DISABLED)

def start_server():
    ip = entry_ip.get()
    port = entry_port.get()
    password = entry_password.get()

    if not ip or not port or not password:
        messagebox.showerror("Error", "All fields are required!")
        return

    # Disable the start button and change color
    button_start.config(state=tk.DISABLED, bg="#AAAAAA", text="Server Running")
    button_stop.config(state=tk.NORMAL)

    start_server_thread(ip, port, password)

def create_server_gui():
    global entry_ip, entry_port, entry_password, chat_area, button_start, button_stop

    root = tk.Tk()
    root.title("Chat Room Server")

    # Top frame for inputs
    top_frame = tk.Frame(root, bg="#128C7E", height=100)
    top_frame.pack(fill=tk.X)

    top_label = tk.Label(top_frame, text="Start Chat Room Server", fg="white", bg="#128C7E", font=("Helvetica", 16))
    top_label.pack(pady=10)

    # IP Address input
    label_ip = tk.Label(top_frame, text="IP Address:", fg="white", bg="#128C7E", font=("Helvetica", 12))
    label_ip.pack(side=tk.LEFT, padx=10, pady=10)
    entry_ip = tk.Entry(top_frame, font=("Helvetica", 14))
    entry_ip.pack(side=tk.LEFT, padx=5, pady=10)

    # Port input
    label_port = tk.Label(top_frame, text="Port:", fg="white", bg="#128C7E", font=("Helvetica", 12))
    label_port.pack(side=tk.LEFT, padx=10, pady=10)
    entry_port = tk.Entry(top_frame, font=("Helvetica", 14))
    entry_port.pack(side=tk.LEFT, padx=5, pady=10)

    # Password input
    label_password = tk.Label(top_frame, text="Password:", fg="white", bg="#128C7E", font=("Helvetica", 12))
    label_password.pack(side=tk.LEFT, padx=10, pady=10)
    entry_password = tk.Entry(top_frame, font=("Helvetica", 14), show='*')
    entry_password.pack(side=tk.LEFT, padx=5, pady=10)

    # Start server button
    button_start = tk.Button(top_frame, text="Start Server", bg="#25D366", fg="white", font=("Helvetica", 14),
                             command=start_server)
    button_start.pack(side=tk.LEFT, padx=10, pady=10)

    # Stop server button
    button_stop = tk.Button(top_frame, text="Stop Server", bg="#FF0000", fg="white", font=("Helvetica", 14),
                            command=stop_server, state=tk.DISABLED)
    button_stop.pack(side=tk.RIGHT, padx=10, pady=10)

    # Chat area
    chat_area = tk.Text(root, wrap=tk.WORD, font=("Helvetica", 12), bg="#ECE5DD")
    chat_area.config(state=tk.DISABLED)
    chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    root.mainloop()

if __name__ == "__main__":
    create_server_gui()
