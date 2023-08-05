import requests


class Logger:

    def __init__(self, is_production, token, program):
        self.server_url = '' if is_production else 'http://127.0.0.1:8000'
        self.token = token
        self.program = program

    def request_post(self, url, data):
        return requests.post(url, data=data, headers={
            'Authorization': f'Token {self.token}'
        })

    def log_error(self, msg):
        return self.request_post(f'{self.server_url}/logs/errors/', {
            'program': self.program,
            'msg': msg,
        })
