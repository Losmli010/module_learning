import socket
import time


def time_server():
    server = socket.socket()     # 创建服务端socket对象

    ip_port = ("", 8220)
    server.bind(ip_port)      # 绑定服务端IP和port

    server.listen(5)        # 服务端监听请求,随时准备接受客户端发来的连接

    while True:
        # accept(): tcp三次握手过程, 耗时操作, 会处于阻塞状态
        # 返回值:tuple(conn, address), conn表示连接到的socket对象,address表示连接到的客户端IP
        conn, address = server.accept()
        print("Got a connection from %s" % str(address))
        response = conn.recv(1024)  # 服务端接收数据, 接收到的数据是字节
        print(response.decode("utf-8"))

        time_str = "Now is: " + time.ctime(time.time()) + "\r\n"
        conn.send(time_str.encode("utf-8"))         # 向客户端发送数据

    server.close()      # tcp四次挥手过程,关闭服务端


if __name__ == "__main__":
    time_server()
