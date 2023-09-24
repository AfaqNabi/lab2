import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 8888        # Port to listen on (non-privileged ports are > 1023)
BYTES_TO_RECEIVE = 4096


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        handle_connection(conn, addr)


def handle_connection(conn, addr):
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(BYTES_TO_RECEIVE)
            if not data:
                break
            print('Received', repr(data))
            conn.sendall(data)


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
