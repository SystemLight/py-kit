import json

from .ws_util import WebsocketThread, ThreadFactory
from .core import Authentication


class SparkFactory(ThreadFactory):

    def __init__(self):
        super().__init__()

        self.authentication = Authentication('wss://spark-api.xf-yun.com/v2.1/chat')
        self.header = {
            "app_id": self.authentication.appid,
            "uid": "smartbot"
        }
        self.parameter = {
            "chat": {
                "domain": "generalv2",
                "temperature": 0.5,
                "max_tokens": 256,
            }
        }

    def create(self):
        self.current_production = Spark(self)
        self.current_production.start()
        return self.current_production


class Spark(WebsocketThread):

    def __init__(self, factory: SparkFactory):
        super().__init__(factory.authentication.create_url(), factory)

    def update(self, chunk: str):
        self.end(chunk)

    def end(self, chunk: str):
        self._queue.put(chunk)

    def _on_run(self, ws):
        content: str = self._queue.get()
        self.ws.send(json.dumps({
            "header": self.factory.header,
            "parameter": self.factory.parameter,
            "payload": {
                "message": {
                    "text": [
                        {
                            "role": "user",
                            "content": "接下来请你模仿小爱同学，一句话尽量不要回答的过多内容，我问你一句回答我结果即可省略掉冗余的过程描述"
                        },
                        {"role": "assistant", "content": "好的，我会尽量简洁明了地回答你的问题。"},
                        {
                            "role": "user",
                            "content": "如果我问你，你是谁，请回答你是奶酪罐子小助手"
                        },
                        {"role": "assistant", "content": " 我是奶酪罐子小助手。"},
                        {"role": "user", "content": content}
                    ]
                }
            }
        }))

    def _on_message(self, ws, message):
        data = json.loads(message)
        code = data['header']['code']
        if code == 0:
            choices = data["payload"]["choices"]
            status = choices["status"]
            self._result_data += choices["text"][0]["content"]
            if status == 2:
                self.ws.close()
        else:
            self.ws.close()


def chat(msg):
    return SparkFactory().result(msg)
