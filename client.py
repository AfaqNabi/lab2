import socket

BYTES_TO_RECEIVE = 4096


def get(host, port):
    request = b'GET / HTTP/1.1\r\nHost: ' + host.encode() + b'\r\n\r\n'
    print(request)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send(request)
    s.shutdown(socket.SHUT_WR)
    result = s.recv(BYTES_TO_RECEIVE)
    while (len(result) > 0):
        print(result)
        result = s.recv(BYTES_TO_RECEIVE)
    s.close()


# get('www.google.com', 80)
get('loaclhost', 8888)
