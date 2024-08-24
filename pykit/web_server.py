import cgi
import json
import os
import shutil
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

cwd_path = os.getcwd()


def fiber(start=None, end=None):
    def decorator(func):
        def wrap(*args):
            def task():
                if start:
                    start(*args)
                func(*args)
                if end:
                    end(*args)

            Thread(target=task).start()

        return wrap

    return decorator


class AppHttpRequestHandler(BaseHTTPRequestHandler):
    UPLOAD_FOLDER = os.path.abspath(os.path.join(cwd_path, './lisys_dist_temp'))

    @staticmethod
    def create_upload_folder():
        if not os.path.exists(AppHttpRequestHandler.UPLOAD_FOLDER):
            os.mkdir(AppHttpRequestHandler.UPLOAD_FOLDER)

    @staticmethod
    def remove_upload_folder():
        try:
            shutil.rmtree(AppHttpRequestHandler.UPLOAD_FOLDER)
        except Exception:
            ...

    @staticmethod
    def save_chunk(context):
        chunk_name = 'chunk_' + str(context['block'])
        chunk_path = os.path.join(AppHttpRequestHandler.UPLOAD_FOLDER, chunk_name)
        with open(chunk_path, 'wb') as fp:
            fp.write(context['file'])

    @staticmethod
    def merge_chunk(context):
        target_name = os.path.join(AppHttpRequestHandler.UPLOAD_FOLDER, context['name'])

        with open(target_name, 'wb') as fpw:
            for i in range(context['total']):
                with open(os.path.join(AppHttpRequestHandler.UPLOAD_FOLDER, 'chunk_' + str(i)), 'rb') as fpr:
                    fpw.write(fpr.read())

        shutil.move(target_name, os.path.join(cwd_path, context['name']))

    def do_GET(self):
        print(self.path)
        self.ok(self.path)

    def do_POST(self):
        if self.path == '/upload':
            # 分片上传文件
            try:
                self.upload_file()
            except Exception as e:
                print(e)
                self.error("上传失败")
        else:
            self.error("接口不存在")

    def log_message(self, _format, *args):
        ...

    def upload_file(self):
        form_data = self.get_form_data()
        file = form_data.getfirst('file')
        block = int(form_data.getfirst('block'))
        total = int(form_data.getfirst('total'))
        md5 = form_data.getfirst('md5')
        name = form_data.getfirst('name')

        context = {
            'file': file,
            'block': block,
            'total': total,
            'md5': md5,
            'name': name
        }

        print('上传文件', block, total, name)

        if file:
            if block == 0:
                AppHttpRequestHandler.remove_upload_folder()
                AppHttpRequestHandler.create_upload_folder()

            AppHttpRequestHandler.save_chunk(context)

            if block >= total - 1:
                AppHttpRequestHandler.merge_chunk(context)
                AppHttpRequestHandler.remove_upload_folder()

            self.ok('上传成功')
        else:
            self.error('上传失败')

    def get_form_data(self):
        return cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={
                'REQUEST_METHOD': 'POST',
                'CONTENT_TYPE': self.headers['Content-Type'],
                'REQUEST_URI': self.path
            }
        )

    def ok(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'status': 200, 'msg': 'ok', 'data': data}).encode())

    def error(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'status': 400, 'msg': 'error', 'data': data}).encode())

    def write_source_body(self):
        with open('raw.txt', 'wb') as fp:
            fp.write(self.rfile.read(int(self.headers['Content-Length'])))
        self.ok("解析")


def server():
    port = 8099
    httpd = HTTPServer(('', port), AppHttpRequestHandler)
    print('Starting httpd... ' + str(port))
    httpd.serve_forever()
    httpd.server_close()


if __name__ == '__main__':
    server()
