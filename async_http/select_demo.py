import select
import types
from collections import deque
import socket
import time


class Task(object):
    """
    运行任务的对象
    """
    def __init__(self, target):
        self.target = target        # 一个协程
        self.sendval = None         # 恢复时要发送的值
        self.stack = []             # 调用栈

    def run(self):
        try:
            result = self.target.send(self.sendval)
            if isinstance(result, SystemCall):
                return result
            if isinstance(result, types.GeneratorType):
                self.stack.append(self.target)
                self.sendval = None
                self.target = result
            else:
                if not self.stack:
                    return
                self.sendval = result
                self.target = self.stack.pop()
        except StopIteration:
            if not self.stack:
                return
            self.sendval = None
            self.target = self.stack.pop()


class SystemCall(object):
    """
    表示系统调用的对象
    """
    def handle(self, sched, task):
        pass


class Scheduler(object):
    """
    调度程序对象
    """
    def __init__(self):
        self.task_queue = deque()
        self.read_waiting = {}
        self.write_waiting = {}
        self.task_num = 0

    def new(self, target):
        """
        通过协程新建任务
        :param target:
        :return:
        """
        new_task = Task(target)
        self.schedule(new_task)
        self.task_num += 1

    def schedule(self, task):
        self.task_queue.append(task)

    def read_wait(self, task, fd):
        """
        让任务等待文件描述符上的数据
        :param task:
        :param fd:
        :return:
        """
        self.read_waiting[fd] = task

    def write_wait(self, task, fd):
        """
        让任务等待写入文件描述符
        :param task:
        :param fd:
        :return:
        """
        self.write_waiting[fd] = task

    def main_loop(self, count=-1, timeout=None):
        """
        调度程序主循环
        :param count:
        :param timeout:
        :return:
        """
        while self.task_num:
            if self.read_waiting or self.write_waiting:
                wait = 0 if self.task_queue else timeout
                r, w, e = select.select(self.read_waiting, self.write_waiting, [], wait)
                for fileno in r:
                    self.schedule(self.read_waiting.pop(fileno))
                for fileno in w:
                    self.schedule(self.write_waiting.pop(fileno))

            # 运行队列中的所有任务
            while self.task_queue:
                task = self.task_queue.popleft()
                try:
                    result = task.run()
                    if isinstance(result, SystemCall):
                        result.handle(self, task)
                    else:
                        self.schedule(task)
                except StopIteration:
                    self.task_num -= 1
            else:
                if count > 0:
                    count -= 1
                if count == 0:
                    return


class ReadWait(SystemCall):
    def __init__(self, f):
        self.f = f

    def handle(self, sched, task):
        fileno = self.f.fileno()
        sched.read_wait(task, fileno)


class WriteWait(SystemCall):
    def __init__(self, f):
        self.f = f

    def handle(self, sched, task):
        fileno = self.f.fileno()
        sched.write_wait(task, fileno)


class NewTask(SystemCall):
    def __init__(self, target):
        self.target = target

    def handle(self, sched, task):
        sched.new(self.target)
        sched.schedule(task)


def time_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("", port))
    server.listen(5)
    while True:
        yield ReadWait(server)
        conn, address = server.accept()
        print("Got a connection from %s" % str(address))
        response = conn.recv(1024)  # 服务端接收数据, 接收到的数据是字节
        print(response.decode("utf-8"))
        yield WriteWait(conn)
        res = time.ctime() + "\r\n"
        conn.send(res.encode("utf-8"))
        conn.close()


if __name__ == '__main__':
    sched = Scheduler()
    sched.new(time_server(8010))
    sched.new(time_server(8020))
    sched.main_loop()
