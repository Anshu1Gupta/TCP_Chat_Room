import threading
import socket

host = '127.0.0.1'
port = 59000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
aliases = []
running = True  # A flag to keep the server running

def broadcast(message):
    for client in clients:
        client.send(message)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            if message.decode('utf-8') == "/exit":
                break  # If the client sends '/exit', close the connection
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f'{alias} has left the chat room!'.encode('utf-8'))
            aliases.remove(alias)
            break

def receive():
    while running:  # Keep running the server until running is set to False
        print('Server is running and listening ...')
        client, address = server.accept()
        print(f'connection is established with {str(address)}')
        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024)
        aliases.append(alias)
        clients.append(client)
        print(f'The alias of this client is {alias}'.encode('utf-8'))
        broadcast(f'{alias} has connected to the chat room'.encode('utf-8'))
        client.send('you are now connected!'.encode('utf-8'))
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

def shutdown_server():
    global running
    running = False
    # Close all client connections
    for client in clients:
        client.close()
    # Close the server socket
    server.close()
    print("Server has been shut down.")

if __name__ == "__main__":
    try:
        receive()
    except KeyboardInterrupt:
        print("KeyboardInterrupt received. Shutting down server...")
        shutdown_server()
