import socket

BYTES_TO_RECEIVE = 4096


def get(host, port):
    request = b'GET / HTTP/1.1\r\nHost: www.google.com\n\n'
    print(request)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.send(request)
        s.shutdown(socket.SHUT_WR)
        result = b'' + s.recv(BYTES_TO_RECEIVE)
        while (len(result) > 0):
            print(result)
            result = s.recv(BYTES_TO_RECEIVE)
        s.close()
        return result


# get('www.google.com', 80)
print(get('loaclhost', 8080))
