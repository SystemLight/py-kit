import socket
import selectors

selector = selectors.DefaultSelector()


class Future:

    def __init__(self):
        self.result = None
        self._callbacks = []

    def add_done_callback(self, fn):
        self._callbacks.append(fn)

    def set_result(self, result):
        self.result = result
        for fn in self._callbacks:
            fn(self)


class Task:

    def __init__(self, coro):
        self.coro = coro
        f = Future()
        f.set_result(None)
        self.step(f)

    def step(self, future):
        try:
            next_future = self.coro.send(future.result)
        except StopIteration:
            return

        next_future.add_done_callback(self.step)


class Client:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.resp = b''

    def connect(self):
        self.sock.setblocking(False)
        try:
            self.sock.connect(('127.0.0.1', 8000))
        except BlockingIOError:
            pass
        f = Future()

        def on_connection():
            f.set_result(None)

        selector.register(self.sock.fileno(), selectors.EVENT_WRITE, on_connection)
        yield f
        selector.unregister(self.sock.fileno())
        self.sock.sendall(b"hello")

        while True:
            f = Future()

            def on_read():
                f.set_result(self.sock.recv(4096))

            selector.register(self.sock.fileno(), selectors.EVENT_READ, on_read)
            chunk = yield f
            selector.unregister(self.sock.fileno())
            if chunk:
                self.resp += chunk
            else:
                break
            print(self.resp)


if __name__ == '__main__':
    c = Client()
    Task(c.connect())
    while True:
        try:
            events = selector.select()
        except OSError:
            break
        for key, mask in events:
            callback = key.data
            callback()
