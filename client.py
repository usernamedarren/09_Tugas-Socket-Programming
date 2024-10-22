import socket

# Konfigurasi Client UDP
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
buffer_size = 1024

# Membuat Socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Mengirim pesan ke server
def send_message(message):
    sock.sendto(message.encode('utf-8'), (UDP_IP, UDP_PORT))
    data, server = sock.recvfrom(buffer_size)
    print(f"Server reply: {data.decode('utf-8')}")

# Example
if __name__ == "__main__":
    while True:
        msg = input("Enter message to send: ")
        send_message(msg)
