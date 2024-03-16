import ssl
from queue import Queue
from threading import Thread

import websocket

websocket.enableTrace(False)


class ThreadFactory:

    def __init__(self):
        self.current_production = None

    def create(self) -> "ProductThread":
        raise NotImplementedError

    def result(self, data):
        p = self.create()
        p.end(data)
        return p.result()


class ProductThread(Thread):

    def __init__(self, factory):
        super().__init__(daemon=True)

        self.factory = factory
        self._result_data = ''

    def update(self, data):
        raise NotImplementedError

    def end(self, data):
        raise NotImplementedError

    def result(self):
        self.join()
        return self._result_data


class WebsocketThread(ProductThread):

    def __init__(self, url, factory):
        super().__init__(factory)

        self.ws = websocket.WebSocketApp(
            url,
            on_open=self._on_open,
            on_message=self._on_message,
            on_close=self._on_close
        )
        self._queue = Queue()

    def run(self) -> None:
        self.ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    def _on_open(self, ws):
        t = Thread(target=self._on_run, args=[ws])
        t.setDaemon(True)
        t.start()

    def _on_run(self, ws):
        raise NotImplementedError

    def _on_message(self, ws, message):
        raise NotImplementedError

    def _on_close(self, ws, close_status_code, close_msg):
        ...
