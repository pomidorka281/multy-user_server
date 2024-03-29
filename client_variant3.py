import os
import socket
import datetime
import json


def main_func(taskstr):
    tasklist = taskstr.split('\n')
    PID_arr = []
    TTY_arr = []
    TIME_arr = []
    CMD_arr = []
    for i in range(1, len(tasklist) - 1):
        j = tasklist[i].split()
        PID_arr.append(j[0])
        TTY_arr.append(j[1])
        TIME_arr.append(j[2])
        if len(j) > 4:
            s = ''
            for k in range(3, len(j)):
                s += j[k]
        else:
            s = j[3]
        CMD_arr.append(s)
    taskdict = {'tasklist': []}
    for i in range(len(PID_arr)):
        taskdict['tasklist'].append({PID_arr[i]: {'TTY': TTY_arr[i], 'TIME': TIME_arr[i], 'CMD': CMD_arr[i]}})

    now = datetime.datetime.now()
    date_date = now.strftime("%d-%m-%Y")
    date_time = now.strftime("%H:%M:%S")
    filename = f"{date_date}/{date_time}.json"
    try:
        os.mkdir(date_date)
    except FileExistsError:
        pass
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(taskdict, file, indent=4, ensure_ascii=False)
    return filename


sock = socket.socket()
sock.connect(('localhost', 9090))  # 192.168.1.9
flag = True

while flag:
    message = input('введите команду, которую хотите отправить: ')
    sock.send(message.encode())
    if message == 'close':
        flag = False
    elif message != 'update':
        print(sock.recv(1024).decode())
    elif message == 'update':
        MSGLEN = int(sock.recv(1024).decode())
        sock.send(b'pass')
        bytes_recd = 0
        data = ''
        while bytes_recd < MSGLEN:
            chunk = sock.recv(min(MSGLEN - bytes_recd, 2048))
            bytes_recd = bytes_recd + len(chunk)
            data += chunk.decode()
        main_func(data)
        print('Success!!!')

sock.close()
