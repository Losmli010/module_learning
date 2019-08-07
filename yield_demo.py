from collections import deque


def foo():
    for i in range(10):
        print("i'm foo %d" % i)
        yield


def bar():
    for i in range(4):
        print("i'm bar %d" % i)
        yield


def spam():
    for i in range(6):
        print("i'm spam %d" % i)
        yield


def func():
    task_queue = deque(maxlen=3)
    task_queue.append(foo())
    task_queue.append(bar())
    task_queue.append(spam())

    while task_queue:
        task = task_queue.pop()
        try:
            next(task)
            task_queue.appendleft(task)
        except StopIteration:
            pass


if __name__ == '__main__':
    func()
