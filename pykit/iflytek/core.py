import base64
import hashlib
import hmac
from datetime import datetime
from time import mktime
from urllib.parse import urlencode, urlparse
from wsgiref.handlers import format_date_time

APPID = ''
APIKEY = ''
API_SECRET = ''


class Authentication:

    def __init__(self, url, appid=APPID, apikey=APIKEY, api_secret=API_SECRET):
        self.url = url
        self.url_obj = urlparse(self.url)
        self.host = self.url_obj.netloc
        self.path = self.url_obj.path
        self.appid = appid
        self.apikey = apikey
        self.api_secret = api_secret

    def create_url(self):
        # 生成RFC1123格式的时间戳
        rfc1123_time = format_date_time(mktime(datetime.now().timetuple()))

        # 签名认证通过hmac-sha256进行加密
        signature = base64.b64encode(hmac.new(
            self.api_secret.encode('utf-8'),
            f'host: {self.host}\ndate: {rfc1123_time}\nGET {self.path} HTTP/1.1'.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()).decode(encoding='utf-8')

        authorization = base64.b64encode(
            f'api_key="{self.apikey}", '
            f'algorithm="hmac-sha256", '
            f'headers="host date request-line", '
            f'signature="{signature}"'.encode('utf-8')
        ).decode(encoding='utf-8')

        return self.url + '?' + urlencode({
            "authorization": authorization,
            "date": rfc1123_time,
            "host": self.host
        })
