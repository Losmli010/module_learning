import sys, time, queue
from multiprocessing.managers import BaseManager

class QueueManager(BaseManager):
    pass

QueueManager.register('get_task_queue')
QueueManager.register('get_result_queue')

server_add = '127.0.0.1'
print('Connect to server %s...' % server_add)
manager = QueueManager(address=(server_add, 5000), authkey=b'abc')
manager.connect()
task = manager.get_task_queue()
result = manager.get_result_queue()
for i in range(10):
    try:
        n = task.get(timeout=1)
        print('Run task %d * %d...' % (n, n))
        r = '%d * %d = %d' % (n, n, n*n)
        time.sleep(1)
        result.put(r)
    except queue.Empty:
        print('task queue is empty.')
print('worker exit.')