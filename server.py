# server.py
import asyncio
import websockets

PASSWORD = "pass"
connected_clients = set()

async def handle_client(websocket, path):
    try:
        await websocket.send("Enter the password:")
        password = await websocket.recv()
        
        if password != PASSWORD:
            await websocket.send("Invalid password. Connection closed.")
            return

        await websocket.send("Welcome to the chatroom!")
        connected_clients.add(websocket)

        async for message in websocket:
            await broadcast(message, websocket)
    except websockets.ConnectionClosed:
        pass
    finally:
        connected_clients.remove(websocket)

async def broadcast(message, sender_websocket):
    for client in connected_clients:
        if client != sender_websocket:
            try:
                await client.send(message)
            except websockets.ConnectionClosed:
                connected_clients.remove(client)

async def main():
    async with websockets.serve(handle_client, "localhost", 5500):
        print("Server started on ws://localhost:8000")
        await asyncio.Future()  # Run forever

asyncio.run(main())
