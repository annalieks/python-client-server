import socket
import threading
import logging
import time
from fsmanager import FSManager
from message import Message
from logger import Logger


class Server:
    header_size: int = 1
    body_size: int = 255
    logfile: str = 'log_server.log'
    info_msg = 'Hello! Server by Anna Alieksieienko. Number 6, files list'
    error_msg = 'Incorrect command!'

    def __init__(self, port):
        self.port = port
        self.socket = socket.socket()
        self.socket.bind(('', self.port))
        self.fs_manager = FSManager()
        self.logger = Logger(self.logfile).get()

    def run(self):
        self.socket.listen(5)
        while True:
            (client_socket, address) = self.socket.accept()
            client_socket.settimeout(4)
            threading.Thread(target=self.process_request,
                                 args=(client_socket,)).run()

    def process_request(self, client_socket):
        try:
            while True:
                message = Message()
                commands = self.accept_message(client_socket)

                for command in commands:
                    if command == 'Who':
                        message.append(self.info_msg)
                    else:
                        try:
                            message.append(self.process_fs_request(command))
                        except Exception:
                            message.append(self.error_msg)
                self.send_response(client_socket, message)

        except socket.timeout:
            pass
        except Exception:
            pass
        finally:
            client_socket.close()

    def accept_message(self, client_socket):
        header = client_socket.recv(self.header_size)
        if header != b'1':
            client_socket.close()
            raise AttributeError

        body = client_socket.recv(self.body_size).decode() or ''
        logging.info(body)
        return body.split(';')

    def process_fs_request(self, command):
        args = command.split(':', 1)
        if len(args) > 1:
            search_type, pattern = args
            return self.fs_manager.process(search_type, pattern)

        return self.fs_manager.process(command)

    @staticmethod
    def send_response(client_socket, message):
        client_socket.send(message.compose())


if __name__ == '__main__':
    Server(1031).run()
