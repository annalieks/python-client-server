import socket
from message import Message
from logger import Logger


class Client:
    header_size: int = 1
    body_size: int = 255
    logfile: str = 'log_client.log'

    def __init__(self, host=None, port=None):
        self.host = host or 'localhost'
        self.port = port or 1031
        self.logger = Logger(self.logfile).get()

    def process_message(self, msg):
        self.socket = socket.socket()
        try:
            self.socket.connect((self.host, self.port))
            self.socket.send(Message(msg).compose())
            self.read_message()
        except Exception:
            print('Server refused to connect')
        self.socket.close()

    def read_message(self):
        header = self.socket.recv(self.header_size)
        if header != b'1':
            print('Wrong response format!')
            return
        body = self.socket.recv(self.body_size).decode()
        print(f'Received response: {body}')
        self.logger.info(body)


if __name__ == '__main__':
    client = Client()

    print('Hi! This is a simple client that supports "files", "dir", '
          '"content" and "Who" commands. Enter your command or "quit" to quit.')
    msg = ''
    while True:
        msg = input()
        if not msg:
            continue
        if msg == 'quit':
            break
        client.process_message(msg)
