from socket import *
import socket
import threading
import logging
import time
import sys


class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        threading.Thread.__init__(self)

    def run(self):
        while True:
            data = self.connection.recv(256)
            if data:
                logging.warning("[SERVER] rcv {} from {}".format(data, self.address))

                if data.startswith(b'TIME') and data.endswith(b'\r\n'):
                    current_time = time.time()
                    readable_time = time.ctime(current_time)
                    response = "JAM {}\r\n".format(readable_time).encode('UTF-8')
                    logging.warning("[SERVER] send {} to {}".format(response, self.address))
                    self.connection.sendall(response)
            else:
                break
        self.connection.close()


class Server(threading.Thread):
    def __init__(self):
        self.the_clients = []
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        threading.Thread.__init__(self)

    def run(self):
        self.my_socket.bind(('0.0.0.0', 45000))
        self.my_socket.listen(1)
        while True:
            self.connection, self.client_address = self.my_socket.accept()
            logging.warning(f"connection from {self.client_address}")

            clt = ProcessTheClient(self.connection, self.client_address)
            clt.start()
            self.the_clients.append(clt)


def main():
    svr = Server()
    svr.start()


if __name__ == "__main__":
    main()
