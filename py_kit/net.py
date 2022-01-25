import socket
from typing import Callable, Union, Optional


class BoundaryFinder:

    def __init__(self, boundary=b'\r\n\x00\r\n'):
        self.boundary = boundary
        self.recv_size = 1024
        self.residual = b''
        self.buffer = []
        self.is_connect = True

    def push(self, chunk: bytes):
        if not chunk:
            self.stop()
            return

        self.residual += chunk

        while True:
            end_index = self.residual.find(self.boundary)

            if end_index == -1:
                break

            cut_pos = end_index + len(self.boundary)
            self.buffer.append(self.residual[0:end_index])
            self.residual = self.residual[cut_pos:]

    def pop(self, text=True, encoding='utf-8'):
        if text:
            data = self.get_text_buffer(encoding)
        else:
            data = self.buffer
        self.buffer = []
        return data

    def clear(self):
        self.residual = b''
        self.buffer = []

    def is_not_residual(self):
        return len(self.residual) == 0

    def get_text_buffer(self, encoding='utf-8'):
        return list(map(lambda v: v.decode(encoding), self.buffer))

    def stop(self):
        self.is_connect = False
        self.clear()

    def handle(self, conn: socket.SocketType, on_data: Callable[["BoundaryFinder", Union[str, bytes]], Optional[bool]]):
        """

        处理连接

        :param conn: socket连接对象
        :param on_data: 返回True则代表立即退出缓冲中已经解包数据被丢弃，否则将继续得到解包数据即使调用stop，直到获取完毕已经解包的内容才退出
        :return:

        """
        while self.is_connect:
            data_buffer = conn.recv(self.recv_size)
            if not data_buffer and self.is_not_residual():
                self.stop()
                break

            self.push(data_buffer)
            for content in self.pop():
                immediately = on_data(self, content)
                if immediately:
                    break


if __name__ == '__main__':
    """

        Client:

            with socket.create_connection(('127.0.0.1', 1083)) as conn:
            conn.sendall(b'asdfasdfasdf\r\n\x00\r\nexitapp\r\n\x00\r\nend of\r\n\x00\r\n3333')
            time.sleep(30)
            conn.sendall(b'23333333\r\n\x00\r\n000000000000000\r\n\x00\r\n')

    """
    local_address = ('127.0.0.1', 1083)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(local_address)
    server.listen(1)

    run_app = True


    def handle_on_data(self: BoundaryFinder, data: str):
        if data == 'exitapp':
            global run_app
            run_app = False
            self.stop()
            return True
        elif data == 'exit':
            self.stop()
            return True
        print(data)


    while run_app:
        remote_connect, remote_address = server.accept()
        print(f'connect: {remote_address}')
        finder = BoundaryFinder()
        finder.handle(remote_connect, handle_on_data)

    server.close()
