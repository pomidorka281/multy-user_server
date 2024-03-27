import socket
import threading
import os

DATA_RECEIVE_BYTE_SIZE = 2**10

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

def get_file_info(path = os.getcwd()):
    file_info = {}

    if os.path.isdir(path):
        file_info['type'] = 'directory'
        file_info['contents'] = []
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            file_info['contents'].append(get_file_info(item_path))
    else:
        file_info['type'] = 'file'
        file_info['size'] = os.path.getsize(path)

    file_info['name'] = os.path.basename(path)
    file_info['path'] = path
    return file_info

server = socket.socket()

server.bind(('', 9090))
server.listen()
count_users = 0

while True:
    client, _ = server.accept()
    count_users += 1
    t = threading.Thread(target=client_thread, args=[client])
    t.start()
