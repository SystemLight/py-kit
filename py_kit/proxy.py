import http.client
import io
import socket
from threading import Thread

from .net import IronSocket


class IronSocketThread(Thread):

    def __init__(self, isock: IronSocket, forward_isock: IronSocket):
        self.isock = isock
        self.forward_isock = forward_isock
        self.is_run = True
        super().__init__()

    def stop(self):
        self.is_run = False
        self.forward_isock.close()

    def run(self) -> None:
        while self.is_run:
            try:
                data_buffer = self.isock.sock.recv(1024)
                if not data_buffer:
                    self.stop()
                self.forward_isock.sock.sendall(data_buffer)
            except (OSError, ConnectionAbortedError):
                self.stop()


class ProxyHttpOrHttps:
    HTTPS_ESTABLISHED = b'HTTP/1.1 200 Connection Established\r\n\r\n'

    def __init__(self, _sock: socket.SocketType):
        self._local_isock = IronSocket(local_proxy_socket)

        http_header: bytes = self._local_isock.read_until_first_boundary()

        http_fp = io.BytesIO(http_header)
        http_header_title = http_fp.readline()
        http_message = http.client.parse_headers(http_fp)
        http_fp.close()

        self.http_method, self.http_url, self.http_version = http_header_title.split(b' ')
        self.host = http_message.get('Host')

        host_args = self.host.split(':')
        self.address = host_args[0]
        if len(host_args) > 1:
            self.port = host_args[1]
        else:
            self.port = 80

        self.conn_address = (self.address, self.port)
        self.http_header = http_header

        self.isock_thread1 = None
        self.isock_thread2 = None

    def _start_interchange(self, _proxy_isock, _local_isock):
        self.isock_thread1 = IronSocketThread(_proxy_isock, _local_isock)
        self.isock_thread2 = IronSocketThread(_local_isock, _proxy_isock)
        self.isock_thread1.setDaemon(True)
        self.isock_thread2.setDaemon(True)
        self.isock_thread1.start()
        self.isock_thread2.start()
        self.isock_thread1.join()
        self.isock_thread2.join()

    def _http_request(self):
        _isock = self._local_isock
        try:
            proxy_isock = IronSocket(socket.create_connection(self.conn_address))
        except TimeoutError as e:
            _isock.close()
            raise e
        proxy_isock.sock.sendall(self.http_header + _isock.get_unread_data())
        self._start_interchange(_isock, proxy_isock)

    def _https_request(self):
        _isock = self._local_isock
        try:
            proxy_isock = IronSocket(socket.create_connection(self.conn_address))
        except TimeoutError as e:
            _isock.close()
            raise e
        _isock.sock.sendall(ProxyHttpOrHttps.HTTPS_ESTABLISHED)
        self._start_interchange(_isock, proxy_isock)

    def start(self):
        if self.http_method == b'CONNECT':
            self._https_request()
        else:
            self._http_request()


class ProxyThread(Thread):

    def __init__(self, sock):
        self.sock = sock
        super().__init__()

        self.setDaemon(True)

    def run(self) -> None:
        try:
            ProxyHttpOrHttps(self.sock).start()
        except ConnectionResetError:
            ...
        print(f'======================Disconnect======================')


if __name__ == '__main__':
    local_address = ('127.0.0.1', 1083)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(local_address)
    server.listen(30)

    run_app = True

    while run_app:
        local_proxy_socket, local_address = server.accept()
        print(f'======================Connect: {local_address}======================')
        ProxyThread(local_proxy_socket).start()

    server.close()
