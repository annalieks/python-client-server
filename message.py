class Message:
    def __init__(self, body=None):
        self.body = body or ''

    def compose(self):
        return b'1' + f'{self.body}'.encode()

    def append(self, msg):
        self.body += f' {msg}'
