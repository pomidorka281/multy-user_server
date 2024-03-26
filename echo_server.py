import socket
import threading
import os


def client_thread(con):
    while True:
        data = con.recv(1024)
        # print(f'Data has been recieved from user number {n}')
        if not data or data.decode() == 'close':
            con.close()
            break
        elif data.decode() == 'update':
            tasklist(con)
        else:
            print('data has been recieved')
            con.send(data)


def tasklist(con):
    if os.name == 'posix':
        taskstr = os.popen('ps -e').read()
    else:
        taskstr = os.popen('tasklist').read()
    taskstr = taskstr.encode('cp1251').decode('cp866')
    con.send(str(len(taskstr)).encode())
    while True:
        if con.recv(1024) == b'pass':
            break
    con.send(taskstr.encode())


server = socket.socket()

server.bind(('', 9090))
server.listen()
count_users = 0

while True:
    client, _ = server.accept()
    count_users += 1
    t = threading.Thread(target=client_thread, args=[client])
    t.start()
