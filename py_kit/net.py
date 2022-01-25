import socket
from typing import Callable, Union, Optional


class IronSockReturnError(Exception):
    ...


class IronSocket:

    def __init__(self, sock: socket.SocketType, timeout=None, boundary=b'\r\n\r\n'):
        """

        IronSocket包含边界读取，满字节读取等扩展功能

        :param sock:
        :param timeout:
        :param boundary:

        """
        self.sock = sock
        self.sock.settimeout(timeout)
        self._timeout = timeout
        self.is_connect = True

        self.boundary = boundary
        self.default_read_size = 1024

        self._buffer = []
        self._residual = b''

    @property
    def pending(self):
        """

        判定是否还存在未处理的边界读取数据

        :return:

        """
        return len(self._residual) != 0

    def set_timeout(self, timeout):
        self.sock.settimeout(timeout)
        self._timeout = timeout

    def get_timeout(self):
        return self._timeout

    def push(self, chunk: bytes):
        """

        读取边界数据时用于填入内容的方法

        :param chunk:
        :return:

        """
        self._residual += chunk

        while True:
            end_index = self._residual.find(self.boundary)

            if end_index == -1:
                break

            cut_pos = end_index + len(self.boundary)
            self._buffer.append(self._residual[0:end_index])
            self._residual = self._residual[cut_pos:]

    def pop(self):
        """

        读取边界数据时用于弹出内容的方法

        :return:

        """
        return self._buffer

    def stop(self):
        self.is_connect = False

    def close(self):
        self.stop()
        self.sock.close()

    def reset_rub(self):
        """

        重置读取边界数据

        :return:

        """
        self._residual = b''
        self._buffer = []

    def read_until_boundary(self, on_data: Callable[["IronSocket", Union[str, bytes]], Optional[bool]]):
        while self.is_connect:
            data_buffer = self.sock.recv(self.default_read_size)
            if not data_buffer:
                raise ConnectionAbortedError('connection lost')

            self.push(data_buffer)
            for content in self.pop():
                on_data(self, content)

    def read(self, buffer_size=None):
        """

        必定会读取到给定字节的数据

        :param buffer_size:
        :return:

        """
        if buffer_size is None:
            buffer_size = self.default_read_size

        read_data = b''
        current_buffer_size = buffer_size
        while True:
            data = self.sock.recv(current_buffer_size)
            if not data:
                raise ConnectionAbortedError('connection lost')

            read_data += data
            read_size = len(read_data)

            if read_size == buffer_size:
                break

            current_buffer_size -= read_size

        return read_data

    def write(self, value):
        self.sock.sendall(value)


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


    def handle_on_data(isock: IronSocket, content: bytes):
        isock.close()
        raise IronSockReturnError(isock, content)


    while run_app:
        remote_connect, remote_address = server.accept()
        try:
            IronSocket(remote_connect).read_until_boundary(handle_on_data)
        except IronSockReturnError as e:
            print(e.args[0].pop())
        except ConnectionAbortedError:
            run_app = False

    server.close()
