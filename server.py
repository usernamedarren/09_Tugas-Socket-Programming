import socket

# Konfigurasi Server UDP
UDP_IP = "127.0.0.1"  # Localhost
UDP_PORT = 5005
buffer_size = 1024

# Membuat Socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Server listening on {UDP_IP}:{UDP_PORT}...")

# Loop untuk menerima dan mengirim pesan
while True:
    data, addr = sock.recvfrom(buffer_size)
    print(f"Received message: {data.decode('utf-8')} from {addr}")
    # Kirim pesan kembali ke client (acknowledgment)
    sock.sendto(f"Message received: {data.decode('utf-8')}".encode(), addr)
