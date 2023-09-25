import socket

BYTES_TO_RECEIVE = 4096


def get(host, port):
    request = b'GET / HTTP/1.1\r\nHost: www.google.com\r\n\r\n'
    print(request)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.send(request)
        s.shutdown(socket.SHUT_WR)
        chunk = s.recv(BYTES_TO_RECEIVE)
        result = b'' + chunk
        while (len(chunk) > 0):
            print(result)
            chunk = s.recv(BYTES_TO_RECEIVE)
            result += chunk
        s.close()
        return result


# get('www.google.com', 80)
print(get('127.0.0.1', 8080))
