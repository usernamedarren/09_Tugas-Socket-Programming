import asyncio
import websockets
import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
buffer_size = 1024

async def handle_client(websocket, path):
    async for message in websocket:
        # Kirim pesan ke server UDP
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(message.encode('utf-8'), (UDP_IP, UDP_PORT))
        data, _ = sock.recvfrom(buffer_size)
        # Kirim balik pesan dari server UDP ke client websocket
        await websocket.send(data.decode('utf-8'))

# Menjalankan WebSocket server
start_server = websockets.serve(handle_client, "localhost", 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
