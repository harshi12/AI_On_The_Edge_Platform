import struct

MAX_CHUNK_SIZE = (64 * 1024)

def send_msg (sock, data):
    if not isinstance(data, bytes):
        data = data.encode()
    length = len(data)
    sock.sendall(struct.pack('!I', length))
    sock.sendall(data)

def recv_msg (sock):
    lengthbuf = recvall(sock, 4)
    if not lengthbuf: return None
    length, = struct.unpack('!I', lengthbuf)
    return recvall(sock, length)

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf
