import socket


def time_client():
    client = socket.socket()          # 创建客户端socket对象
    ip_port = ("127.0.0.1", 8080)  # 服务端IP和port
    client.connect(ip_port)  # 向服务端发起连接请求

    requirement = "What time is now?"
    client.send(requirement.encode("utf-8"))   # 向服务端发送数据

    response = client.recv(1024)                  # 接收来自服务端的数据
    print(response.decode("utf-8"))

    client.close()      # 关闭客户端


if __name__ == "__main__":
    time_client()
