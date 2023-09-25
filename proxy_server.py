import socket
import threading

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 8080        # Port to listen on (non-privileged ports are > 1023)
BYTES_TO_RECEIVE = 4096

# send some data(request) to host:port


def send_request(host, port, request):
    # create a new socket in with block to ensure it's closed once were done
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # connect to host:port
        s.connect((host, port))
        # send data
        s.send(request)
        # shutdown the socket for writing to indicate that we're done sending
        s.shutdown(socket.SHUT_WR)
        # receive data from the socket
        data = s.recv(BYTES_TO_RECEIVE)
        result = b'' + data
        # loop until we receive no more data
        while (len(data) > 0):
            print(result)
            data = s.recv(BYTES_TO_RECEIVE)
            result += data
        # # close the socket
        s.close()
        # return the result
        return result


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.listen(2)
        conn, addr = s.accept()
        handle_connection(conn, addr)


def handle_connection(conn, addr):
    with conn:
        print('Connected by', addr)
        request = b''
        while True:
            data = conn.recv(BYTES_TO_RECEIVE)
            if not data:
                break
            print('Received', repr(data))
            request += data
        resp = send_request('www.google.com', 80, request)
        conn.sendall(resp)


def start_threaded_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.listen(2)
        while True:
            conn, addr = s.accept()
            # create a new thread to handle the connection
            thread = threading.Thread(
                target=handle_connection, args=(conn, addr))
            thread.run()


start_threaded_server()
# start_server()
