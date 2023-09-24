import socket
import threading

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 8888        # Port to listen on (non-privileged ports are > 1023)
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
        result = b'' + s.recv(BYTES_TO_RECEIVE)
        # loop until we receive no more data
        while (len(result) > 0):
            print(result)
            result = s.recv(BYTES_TO_RECEIVE)
        # # close the socket
        # s.close()
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
        while True:
            data = b''+conn.recv(BYTES_TO_RECEIVE)
            if not data:
                break
            print('Received', repr(data))
        resp = send_request('www.google.com', 80, data)
        conn.sendall(resp)

def start_threaded_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            # create a new thread to handle the connection
            threading.Thread(target=handle_connection, args=(conn, addr)).run()

def main():
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Get local machine name
    host = socket.gethostname()
    port = 9999

    # Bind to the port
    s.bind((host, port))

    # Now wait for client connection.
    s.listen(5)

    while True:
        # Establish connection with client.
        c, addr = s.accept()
        print('Got connection from', addr)
        data = c.recv(BYTES_TO_RECEIVE)
        print('Server received', repr(data))

        filename = 'mytext.txt'
        f = open(filename, 'rb')
        l = f.read(BYTES_TO_RECEIVE)
        while (l):
            c.send(l)
            print('Sent', repr(l))
            l = f.read(BYTES_TO_RECEIVE)
        f.close()

        print('Done sending')
        c.send(b'Thank you for connecting')
        c.close()
