import socket
from datetime import datetime
from message_list import *
from rd_functions import *
import msvcrt

def get_mnumber(data):
    return int.from_bytes(data[0:4], byteorder='big')

def get_snumber(data):
    return int.from_bytes(data[4:8], byteorder='big')

def get_msgtype(data):
    return int.from_bytes(data[8:12], byteorder='big')

def find_msg(data):
    msgtype = get_msgtype(data)
    return message_list[msgtype][0][0]

def get_data(data, pointer, datatype):
    if (datatype == 'qint8'):
        return rd_qint8(data, pointer)
    if (datatype == 'quint8') | (datatype == 'bool'):
        return rd_quint8(data, pointer)

    if (datatype == 'qint32'):
        return rd_qint32(data, pointer)
    if (datatype == 'quint32'):
        return rd_quint32(data, pointer)

    if (datatype == 'qint64'):
        return rd_qint64(data, pointer)
    if (datatype == 'quint64'):
        return rd_quint64(data, pointer)

    if datatype == 'float':
        return rd_floatd(data, pointer)
    if datatype == 'QTime':
        return rd_qtime(data, pointer)
    if datatype =='QDate':
        return rd_qdate(data, pointer)
    if datatype == 'QDateTime':
        return rd_qdatetime(data, pointer)
    if datatype =='utf8':
        return rd_utf8(data, pointer)
    return 'something ERROR!'

def print_msgs(data):
    index = get_msgtype(data)
    print(f'****{message_list[index][0][0]}****')
    pointer = 12
    for i, outdata in enumerate(message_list[index][1]):
        #print(f'{message_list[index][1][i][0]}({outdata[1]})')
        result = get_data(data, pointer, outdata[1])
        pointer = result[1]
        print(f'{message_list[index][1][i][0]}({outdata[1]})Value:{result[0]}(PTR:{pointer})')


if __name__ == "__main__":
    server_address =('localhost', 6789)
    max_size = 4096

    try:
        with open('server_address.dat') as f:
            ft = f.read()
    except:
        print ("server_address.dat open error")
        ss = input("enter something to exit")
        errorflag = 1


    #ft = ('localhost,6789')
    fsplit = ft.split(',')
    server_address = (fsplit[0], int(fsplit[1])) 

    print('Starting the server at', datetime.now())
    print ('Waiting for client to call.')
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(server_address)
    
    while 1:
        
        if msvcrt.kbhit():
            server.close()
            break
        else:
            data, client = server.recvfrom(max_size)
            #print('At', datetime.now(), client, 'said', data)
            print(f'At{datetime.now()}')
            #print(f'Magic Number = {get_mnumber(data) : 08x}')
            #print(f'Schema Number = {get_snumber(data) : 08x}')
            #print(f'Message type = {get_msgtype(data) : 08x}')
            print_msgs(data)
            #print(f'Message name ={find_msg(data)}')
            #server.sendto(b'Are you talking to me?', client)
            