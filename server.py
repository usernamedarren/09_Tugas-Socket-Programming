import socket
import threading
import tkinter as tk
from tkinter import messagebox

# Global variables
clients = {}
server_password = ""  # Will be set through the GUI
server_socket = None

# Function to handle client communication
def handle_client(server_socket, log_area):
    while True:
        try:
            # Receive message from client
            message, client_address = server_socket.recvfrom(1024)
            decoded_message = message.decode()

            if client_address in clients:
                # Broadcast message to all clients except the sender
                for client in clients:
                    if client != client_address:
                        server_socket.sendto(f"{clients[client_address]}: {decoded_message}".encode(), client)
                log_area.insert(tk.END, f"Message from {clients[client_address]}: {decoded_message}\n")
            else:
                # First message must be the password
                if decoded_message == server_password:
                    server_socket.sendto("Password accepted! Please enter your username:".encode(), client_address)
                    username, _ = server_socket.recvfrom(1024)
                    username = username.decode().strip()

                    # Save client to the dict
                    if username and client_address not in clients:
                        clients[client_address] = username
                        log_area.insert(tk.END, f"New client connected: {username} ({client_address})\n")

                        # Notify all clients about the new client
                        broadcast_message = f"{username} has joined the chatroom."
                        for client in clients:
                            if client != client_address:
                                server_socket.sendto(broadcast_message.encode(), client)
                    else:
                        server_socket.sendto("Invalid username!".encode(), client_address)
                else:
                    server_socket.sendto("Incorrect password, connection denied.".encode(), client_address)

        except Exception as e:
            log_area.insert(tk.END, f"Server error: {e}\n")

# Function to start the server
def start_server(server_ip, server_port, password, log_area):
    global server_password, server_socket
    server_password = password

    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((server_ip, int(server_port)))

    log_area.insert(tk.END, f"UDP server started on {server_ip}:{server_port}\n")

    # Start a thread to handle client messages
    threading.Thread(target=handle_client, args=(server_socket, log_area), daemon=True).start()

# Function to handle the "Start Server" button click
def start_server_gui(ip_entry, port_entry, password_entry, log_area):
    server_ip = ip_entry.get()
    server_port = port_entry.get()
    password = password_entry.get()

    if not server_ip or not server_port or not password:
        messagebox.showerror("Input Error", "All fields must be filled!")
        return

    try:
        start_server(server_ip, server_port, password, log_area)
    except Exception as e:
        log_area.insert(tk.END, f"Error starting server: {e}\n")

# Function to create the GUI window
def create_server_gui():
    root = tk.Tk()
    root.title("Server GUI")

    # Server IP input
    tk.Label(root, text="Server IP:").grid(row=0, column=0, padx=10, pady=5)
    ip_entry = tk.Entry(root)
    ip_entry.grid(row=0, column=1, padx=10, pady=5)

    # Server Port input
    tk.Label(root, text="Server Port:").grid(row=1, column=0, padx=10, pady=5)
    port_entry = tk.Entry(root)
    port_entry.grid(row=1, column=1, padx=10, pady=5)

    # Password input
    tk.Label(root, text="Password:").grid(row=2, column=0, padx=10, pady=5)
    password_entry = tk.Entry(root, show="*")
    password_entry.grid(row=2, column=1, padx=10, pady=5)

    # Log area (for showing server messages and connected clients)
    log_area = tk.Text(root, height=15, width=50)
    log_area.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    # Start Server button
    start_button = tk.Button(root, text="Start Server", command=lambda: start_server_gui(ip_entry, port_entry, password_entry, log_area))
    start_button.grid(row=3, column=0, columnspan=2, pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_server_gui()
