# server.py
import asyncio
import websockets

# Configuration
PASSWORD = "pass"  # Replace with the required password for the chatroom
connected_clients = set()  # Store the connected clients

# Function to handle client connections
async def handle_client(websocket, path):
    try:
        # Ask for a password
        await websocket.send("Enter the password:")
        password = await websocket.recv()

        # Check if the password matches
        if password != PASSWORD:
            await websocket.send("Invalid password. Connection closed.")
            return  # Close the connection if the password is incorrect

        await websocket.send("Welcome to the chatroom!")
        connected_clients.add(websocket)

        # Listen for incoming messages from the client
        async for message in websocket:
            await broadcast(message, websocket)
    except websockets.ConnectionClosed:
        print("A client disconnected.")
    finally:
        # Remove the client from the set of connected clients
        connected_clients.remove(websocket)

# Function to broadcast messages to all connected clients except the sender
async def broadcast(message, sender_websocket):
    for client in connected_clients:
        if client != sender_websocket:
            try:
                await client.send(message)
            except websockets.ConnectionClosed:
                connected_clients.remove(client)

# Main function to start the WebSocket server
async def main():
    server = await websockets.serve(handle_client, "localhost", 8000)
    print("Server started on ws://localhost:8000")
    await server.wait_closed()

# Run the server
if __name__ == "__main__":
    asyncio.run(main())
