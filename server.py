import socket
import threading

# Global variables
clients = {}
password = "chatpassword"  # Password yang harus dimasukkan client

def handle_client(server_socket):
    while True:
        # Terima pesan dari client
        try:
            message, client_address = server_socket.recvfrom(1024)
            decoded_message = message.decode()

            if client_address in clients:
                # Broadcast pesan ke semua client kecuali pengirim
                for client in clients:
                    if client != client_address:
                        server_socket.sendto(f"{clients[client_address]}: {decoded_message}".encode(), client)
                print(f"Pesan dari {clients[client_address]}: {decoded_message}")
            else:
                # Pesan pertama harus password, jika tidak sesuai, abaikan client
                if decoded_message == password:
                    server_socket.sendto("Password diterima!".encode(), client_address)
                    username, _ = server_socket.recvfrom(1024)
                    username = username.decode().strip()

                    # Simpan client ke dalam dict
                    clients[client_address] = username
                    print(f"Client baru terhubung: {username} ({client_address})")

                    # Beri tahu semua client tentang client baru
                    broadcast_message = f"{username} telah bergabung ke chatroom."
                    for client in clients:
                        if client != client_address:
                            server_socket.sendto(broadcast_message.encode(), client)
                else:
                    server_socket.sendto("Password salah, koneksi ditolak.".encode(), client_address)

        except Exception as e:
            print(f"Kesalahan di server: {e}")

def start_server():
    server_ip = "127.0.0.1"
    server_port = 12345
    
    # Buat socket UDP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((server_ip, server_port))

    print(f"Server UDP dimulai di {server_ip}:{server_port}")

    # Thread untuk menangani client
    threading.Thread(target=handle_client, args=(server_socket,), daemon=True).start()

    while True:
        pass  # Server terus berjalan


if __name__ == "__main__":
    start_server()
