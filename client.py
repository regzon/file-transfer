#!/usr/bin/env python3

import sys
import socket


def send_message(sock):
    sock.sendall(b'Hello world')
    print("Sent message to the server")


def create_socket(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
    except Exception as e:
        sock.close()
        raise e
    return sock


def main(host, port):
    with create_socket(host, port) as sock:
        send_message(sock)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} host port")
        exit(1)
    main(sys.argv[1], int(sys.argv[2]))
