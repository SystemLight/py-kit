import base64
import json
import threading
import time
from typing import IO, Union, Optional

from .ws_util import WebsocketThread, ThreadFactory
from .core import Authentication


class SpeechRecognitionFactory(ThreadFactory):
    TAG = 'SpeechRecognitionFactory'

    def __init__(self):
        super().__init__()

        self.authentication = Authentication('wss://iat-api.xfyun.cn/v2/iat')
        self.common_args = {
            "app_id": self.authentication.appid
        }
        self.business_args = {
            "domain": "iat",
            "language": "zh_cn",
            "accent": "mandarin",
            "vinfo": 1,
            "vad_eos": 10000
        }
        self.frame_size = 8000
        self.interval = 0.02
        self.rate = 16000
        self.sample_width = 2
        self.sample_second_size = self.sample_width * self.rate

    def create(self):
        self.current_production = SpeechRecognition(self)
        self.current_production.start()
        return self.current_production


class SpeechRecognition(WebsocketThread):
    TAG = 'SpeechRecognition'

    STATUS_FIRST_FRAME = 0  # 第一帧的标识
    STATUS_CONTINUE_FRAME = 1  # 中间帧标识
    STATUS_LAST_FRAME = 2  # 最后一帧的标识

    def __init__(self, factory: SpeechRecognitionFactory):
        super().__init__(factory.authentication.create_url(), factory)

        self.status = SpeechRecognition.STATUS_FIRST_FRAME
        self.current_duration = 0
        self.timer = threading.Timer(1, self.ws.close)

    def _update_data(self, chunk: Union[IO, bytes]):
        if isinstance(chunk, bytes):
            data_size = len(chunk)
            for i in range(data_size // self.factory.frame_size + int(data_size % self.factory.frame_size > 0)):
                start_index = i * self.factory.frame_size
                data = chunk[start_index:start_index + self.factory.frame_size]
                self.current_duration += len(data) / self.factory.sample_second_size
                self._queue.put(data)
        else:
            while True:
                data = chunk.read(self.factory.frame_size)
                if not data:
                    break
                self.current_duration += len(data) / self.factory.sample_second_size
                self._queue.put(data)

    def _send_first_frame(self, buffer: bytes):
        self.ws.send(json.dumps({
            "common": self.factory.common_args,
            "business": self.factory.business_args,
            "data": {
                "status": self.status,
                "format": "audio/L16;rate=16000",
                "audio": str(base64.b64encode(buffer), 'utf-8'),
                "encoding": "raw"
            }
        }))

    def _send_continue_frame(self, buffer: bytes):
        self.ws.send(json.dumps({
            "data": {
                "status": self.status,
                "format": "audio/L16;rate=16000",
                "audio": str(base64.b64encode(buffer), 'utf-8'),
                "encoding": "raw"
            }
        }))

    def _send_last_frame(self, buffer: bytes):
        self.ws.send(json.dumps({
            "data": {
                "status": self.status,
                "format": "audio/L16;rate=16000",
                "audio": str(base64.b64encode(buffer), 'utf-8'),
                "encoding": "raw"
            }
        }))

    def update(self, chunk: Union[IO, bytes]):
        self._update_data(chunk)

    def end(self, chunk: Union[IO, bytes, None] = None):
        if chunk:
            self._update_data(chunk)

        self._queue.put(None)

    def _on_run(self, ws):
        while self.status is not None:
            data: Optional[bytes] = self._queue.get()

            if data is None:
                self.status = SpeechRecognition.STATUS_LAST_FRAME

            if self.status == SpeechRecognition.STATUS_FIRST_FRAME:
                self._send_first_frame(data)
                self.status = SpeechRecognition.STATUS_CONTINUE_FRAME
            elif self.status == SpeechRecognition.STATUS_CONTINUE_FRAME:
                self._send_continue_frame(data)
            elif self.status == SpeechRecognition.STATUS_LAST_FRAME:
                self._send_last_frame(b'')
                self.status = None

            time.sleep(self.factory.interval)

        self.timer.start()

    def _on_message(self, ws, message):
        result_message = json.loads(message)
        code = result_message["code"]

        if code == 0:
            data = result_message["data"]["result"]["ws"]
            for i in data:
                for w in i["cw"]:
                    self.factory.hook.emit('message', [w["w"]])
                    self._result_data += w["w"]

            if self.status is None:
                # 如果已经发送完最后一帧则立即关闭接收认为是最后一次接收
                self.timer.cancel()
                self.ws.close()
        else:
            self.ws.close()

    def _on_close(self, ws, close_status_code, close_msg):
        super()._on_close(ws, close_status_code, close_msg)
