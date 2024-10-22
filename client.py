import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message, _ = client_socket.recvfrom(1024)
            print(f"\n{message.decode()}")
        except Exception as e:
            print(f"Kesalahan saat menerima pesan: {e}")
            break

def start_client():
    server_ip = "127.0.0.1"
    server_port = 12345
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Kirim password ke server
    password = input("Masukkan password untuk bergabung ke chatroom: ")
    client_socket.sendto(password.encode(), (server_ip, server_port))
    
    # Terima respon password
    response, _ = client_socket.recvfrom(1024)
    print(response.decode())
    
    if "Password diterima" in response.decode():
        # Masukkan username
        username = input("Masukkan username: ")
        client_socket.sendto(username.encode(), (server_ip, server_port))
        
        # Jalankan thread untuk menerima pesan dari server
        threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

        # Kirim pesan ke server
        while True:
            message = input()
            if message.strip().lower() == "exit":
                break
            client_socket.sendto(message.encode(), (server_ip, server_port))

    else:
        print("Koneksi ditolak karena password salah.")
    client_socket.close()


if __name__ == "__main__":
    start_client()
