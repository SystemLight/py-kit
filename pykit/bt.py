import hashlib
import json
import time
import urllib.parse
import urllib.request
from pprint import pp


class System:
    _name = 'system'

    get_system_total = f'/{_name}?action=GetSystemTotal'


class Data:
    _name = 'data'

    get_data = f'/{_name}?action=getData'


class BtApi:

    def __init__(self, host, key):
        self.host = host
        self.api_sk = key
        self.api_sk_md5 = self._get_md5(key)

    @staticmethod
    def _get_md5(_content: str):
        return hashlib.md5(_content.encode()).hexdigest()

    def _get_data(self):
        now_time = int(time.time())
        return {
            'request_token': self._get_md5(f'{now_time}{self.api_sk_md5}'),
            'request_time': now_time
        }

    def post(self, action_api: str, **kwargs):
        _data = self._get_data()
        _data |= (kwargs or {})

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
        }

        req = urllib.request.Request(
            self.host + action_api,
            data=urllib.parse.urlencode(_data).encode(),
            method='POST',
            headers=headers
        )

        with urllib.request.urlopen(req) as resp:
            content = resp.read()
        return json.loads(content.decode())


if __name__ == '__main__':
    bt = BtApi('http://localhost:8888', 'your api key')
    pp(bt.post(Data.get_data, table='logs', limit=10, tojs='test'))
    pp(bt.post(System.get_system_total))
