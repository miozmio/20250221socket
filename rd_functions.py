import struct
def rd_qint8(data, pointer):
    incvalue = 1
    v = int.from_bytes(data[pointer:pointer + incvalue], byteorder='big')
    if v >= 0x80:
        v = v - 0x100
    newpointer = pointer + incvalue
    return [v, newpointer]

def rd_quint8(data, pointer):
    incvalue = 1
    v = int.from_bytes(data[pointer:pointer + incvalue], byteorder='big')
    newpointer = pointer + incvalue
    return [v, newpointer]

def rd_qint16(data, pointer):
    incvalue = 2
    v = int.from_bytes(data[pointer:pointer + incvalue], byteorder='big')
    if v >= 0x8000:
        v = v - 0x10000    
    newpointer = pointer + incvalue
    return [v, newpointer]

def rd_quint16(data, pointer):
    incvalue = 2
    v = int.from_bytes(data[pointer:pointer + incvalue], byteorder='big')
    newpointer = pointer + incvalue
    return [v, newpointer]

def rd_qint32(data, pointer):
    incvalue = 4
    v = int.from_bytes(data[pointer:pointer + incvalue], byteorder='big')
    if v >= 0x80000000:
        v = v - 0x100000000
    newpointer = pointer + incvalue
    return [v, newpointer]

def rd_quint32(data, pointer):
    incvalue = 4
    v = int.from_bytes(data[pointer:pointer + incvalue], byteorder='big')
    newpointer = pointer + incvalue
    return [v, newpointer]

def rd_qint64(data, pointer):
    incvalue = 8
    v = int.from_bytes(data[pointer:pointer + incvalue], byteorder='big')
    if v >= 0x8000000000000000:
        v = v - 0x10000000000000000
    newpointer = pointer + incvalue
    return [v, newpointer]

def rd_quint64(data, pointer):
    incvalue = 8
    v = int.from_bytes(data[pointer:pointer + incvalue], byteorder='big')
    newpointer = pointer + incvalue
    return [v, newpointer]

def rd_floatd(data, pointer):
    incvalue = 8
    #v = float.from_bytes(data[pointer:pointer + incvalue], byteorder='big')
    v = struct.unpack('>d', data[pointer:pointer + incvalue])
    newpointer = pointer + incvalue
    return [v, newpointer]

def rd_utf8(data, pointer):
    incvalue = 4
    v = int.from_bytes(data[pointer:pointer + incvalue], byteorder='big')
    if v == 0xffffffff:
        v = 0
    s = data[pointer + incvalue : pointer + incvalue + v]
    newpointer = pointer + incvalue + v
    return [s, newpointer]

def rd_qtime(data, pointer):
    return rd_quint32(data, pointer)

def rd_qdate(data, pointer):
    return rd_quint64(data, pointer)

def rd_qdatetime(data, pointer):
    qdate = rd_qdate(data, pointer)
    qtime = rd_qtime(data, qdate[1])
    timespec = rd_qint8(data, qtime[1])
    newpointer = timespec[1]
    timeoffset = [0, 0]
    if timespec[1] == 2:
        timeoffset = rd_qint32(data, newpointer)
        newpointer = timeoffset[1]
    return [[qdate[0],qtime[0],timespec[0],timeoffset[0]], newpointer]

