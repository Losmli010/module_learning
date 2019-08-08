from http.client import responses
import asynchat, asyncore, socket
import os
import mimetypes


class async_http(asyncore.dispatcher):
    """
    处理请求的实践
    """
    def __init__(self, port):
        super().__init__()
        self.create_socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(("", port))
        self.listen(5)

    def handle_accept(self):
        conn, address = self.accept()
        return async_http_handler(conn)


class async_http_handler(asynchat.async_chat):
    """
    异步处理请求
    """
    def __init__(self, conn):
        super().__init__()
        self.data = []
        self.got_header = False
        self.set_terminator(b"\r\n\r\n")

    # 获取数据并加入缓冲区
    def collect_incoming_data(self, data):
        if not self.got_header:
            self.data.append(data)

    # 到达终止符
    def found_terminator(self):
        self.got_header = True
        header_data = b"".join(self.data)
        header_text = header_data.decode("iso-8859-1")
        header_lines = header_text.splitlines()
        request = header_lines[0].split()
        op = request[0]
        url = request[1][1:]
        self.handle_request(op, url)

    def push_text(self, text):
        self.push(text.encode("iso-8859-1"))

    # 处理请求
    def handle_request(self, op, url):
        if op == "GET":
            if not os.path.exists(url):
                self.send_error(404, "File %s not found\r\n" % url)
            else:
                types, encoding = mimetypes.guess_type(url)
                size = os.path.getsize(url)
                self.push_text("HTTP/1.0 200 OK\r\n")
                self.push_text("Content-length: %s\r\n" % size)
                self.push_text("Content-type: %s\r\n" % types)
                self.push_text("\r\n")
                self.push_with_producer(file_producer(url))
        else:
            self.send_error(501, "%s method not implemented\r\n" % op)

        self.close_when_done()

    def send_error(self, status_code, msg):
        self.push_text("HTTP/1.0 %s %s\r\n" % (status_code, responses[status_code]))
        self.push_text("Content-type: text/plain\r\n")
        self.push_text("\r\n")
        self.push_text(msg)


class file_producer(object):
    def __init__(self, filename, buffer_size=512):
        self.file = open(filename, "rb")
        self.buffer_size = buffer_size

    def more(self):
        data = self.file.read(self.buffer_size)
        if not data:
            self.file.close()
        return data


if __name__ == '__main__':
    a = async_http(8080)
    asyncore.loop()
