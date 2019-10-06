#!/usr/bin/env python3

import os
import sys
import socket

BUFF_SIZE = 1024


def read_file(filename, chunk_size):
    """Yield a chunk of bytes from the file"""
    with open(filename, 'rb') as f:
        chunk = f.read(chunk_size)
        while chunk:
            yield chunk
            chunk = f.read(chunk_size)


def show_progress(sent_size, total_size):
    sys.stdout.write("Uploaded %d of %d bytes\r" % (sent_size, total_size))
    sys.stdout.flush()


def send_file(sock, filename):
    basename = os.path.basename(filename)
    sock.sendall(basename.encode() + b'\0')
    print("Sent file name to the server")
    file_size = os.path.getsize(filename)
    sent_size = 0
    for chunk in read_file(filename, BUFF_SIZE):
        sock.sendall(chunk)
        sent_size += len(chunk)
        show_progress(sent_size, file_size)
    print()
    print("Sent a file to the server")


def create_socket(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
    except Exception as e:
        sock.close()
        raise e
    return sock


def main(filename, host, port):
    with create_socket(host, port) as sock:
        send_file(sock, filename)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} filename host port")
        exit(1)
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]))
