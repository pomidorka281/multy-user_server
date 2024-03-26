import socket
import threading


def client_thread(con):
    while True:
        data = con.recv(1024)
        # print(f'Data has been recieved from user number {n}')
        if not data:
            con.close()
            break
        else:
            con.send(data)


server = socket.socket()

server.bind(('', 9090))
server.listen(5)
count_users = 0

while True:
    client, _ = server.accept()
    count_users += 1
    threading.Thread(target=client_thread(client))
