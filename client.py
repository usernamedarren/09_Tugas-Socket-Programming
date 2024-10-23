import socket
import threading

# Client configuration
SERVER_HOST = 'localhost'
SERVER_PORT = 5500

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except:
            print("Disconnected from the server")
            break

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    
    # Start a thread to listen for messages from the server
    threading.Thread(target=receive_messages, args=(client_socket,)).start()

    # Send password for verification
    password = input("Enter password: ")
    client_socket.send(password.encode('utf-8'))
    
    while True:
        message = input()
        if message.lower() == 'exit':
            break
        client_socket.send(message.encode('utf-8'))

    client_socket.close()

if __name__ == "__main__":
    main()
