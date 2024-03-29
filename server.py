#!/usr/bin/env python3

import socket

from threading import Thread

SERVER_HOST = ''
SERVER_PORT = 8080

BUFF_SIZE = 1024


class ClientListener(Thread):
    """Thread that communicates with a single client"""

    def __init__(self, sock, address):
        super().__init__(daemon=True)
        self.sock = sock
        self.address = address

    def _close(self):
        print(f"Closing a connection from {self.address}")
        self.sock.close()

    def _read_filename(self):
        filename_data = bytes()
        residual_data = bytes()

        while True:
            data = self.sock.recv(BUFF_SIZE)
            if not data:
                break
            index = data.find(b'\0')
            if index != -1:
                filename_data += data[:index]
                if len(data) > index + 1:
                    residual_data += data[index + 1:]
                break
            else:
                filename_data += data

        filename = filename_data.decode()
        return filename, residual_data

    def _read_file(self, filename, initial_data):
        with open('copy_' + filename, 'wb') as f:
            f.write(initial_data)
            while True:
                data = self.sock.recv(BUFF_SIZE)
                if not data:
                    break
                f.write(data)

    def run(self):
        filename, data = self._read_filename()
        print(f"Read file name {filename}")
        self._read_file(filename, data)
        print("Saved a file")
        self._close()


def create_socket(host, port):
    """
    Create a socket with given address and port,
    and start listening to it.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen()
    except Exception as e:
        sock.close()
        raise e
    print("Created server socket")
    return sock


def start_server(sock: socket.socket):
    """Start a server that accepts new connections from a given socket"""
    print("Started the server")
    while True:
        client_sock, client_address = sock.accept()
        print(f"Accepted new connection from {client_address}")
        ClientListener(client_sock, client_address).start()


def main():
    with create_socket(SERVER_HOST, SERVER_PORT) as server_sock:
        start_server(server_sock)


if __name__ == "__main__":
    main()
