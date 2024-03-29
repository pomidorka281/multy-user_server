import socket

DATA_RECEIVE_BYTE_SIZE = 2**10

def socket_connect(host, port):
    client_socket = socket.socket()
    client_socket.connect((host, port))
    return client_socket

def send_command(command, client_socket):
    client_socket.send(command.encode())
    packageLen = int(client_socket.recv(DATA_RECEIVE_BYTE_SIZE).decode())
    bytesReceive = 0
    response = b''

    while bytesReceive < packageLen:
        chunk = client_socket.recv(min(packageLen - bytesReceive, 2048))  
        bytesReceive = bytesReceive + len(chunk)
        response += chunk

    print(response.decode(), '\n')

HOST = '192.168.158.138'
PORT = 9090
client_socket = socket_connect(HOST,PORT)
    
while True:
    print("""
    Available commands:
    1. get_info - Get information about files in current directory
    2. set_root [directory_path] - Set a new root directory
    3. quit - Quit the program
    Enter command: 
    """)
    command = input()
    if command.startswith("set_root"):
        send_command(command, client_socket)
    elif command == "quit":
        break
    else:
        send_command(command, client_socket)
client_socket.close()