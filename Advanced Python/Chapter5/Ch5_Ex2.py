def divide(x,y):
    quotient=x//y
    remainder=x%y
    return(quotient,remainder)
print(divide(8,3))
q,r=divide(8,3)
print(q,r)
import re
m=re.match(r'\d+','abc')
print(m)
m=re.match('\d+','123')
print(m)
from threading import Thread
import threading, time

def task(name):
    print(f"[{name}] start @ {time.time():.2f}")
    time.sleep(1)          # 模拟 I/O（如网络、磁盘）
    print(f"[{name}] end   @ {time.time():.2f}")

# 顺序执行（2秒）
start = time.time()
task("A"); task("B")
print(f"Sequential: {time.time() - start:.2f}s")

# 并发执行（≈1秒）
start = time.time()
t1 = threading.Thread(target=task, args=("A",))
t2 = threading.Thread(target=task, args=("B",))
t1.start(); t2.start()
t1.join(); t2.join()
print(f"Concurrent: {time.time() - start:.2f}s")


counter = 0
num_threads = 100

def unsafe_increment():
    global counter
    for _ in range(10000):          # 增加次数
        current = counter           # 1. 读
        time.sleep(0)               # 2. 强制线程切换点（关键！）
        current += 1                # 3. 改
        counter = current           # 4. 写

threads = [threading.Thread(target=unsafe_increment) for _ in range(num_threads)]
for t in threads: t.start()
for t in threads: t.join()

expected = num_threads * 10000
print(f"Expected: {expected}")
print(f"Actual  : {counter}")
print(f"Lost    : {expected - counter}")

counter = 0
lock = threading.Lock()
num_threads = 100

def safe_increment():
    global counter
    for _ in range(10000):
        with lock:       # 串行化临界区
            counter += 1

threads = [threading.Thread(target=safe_increment) for _ in range(num_threads)]
for t in threads: t.start()
for t in threads: t.join()

print(f"With lock: {counter}")  # 稳定输出 100000

def cpu_bound(n):
    while n > 0: n -= 1  # 纯计算，不释放 GIL

# 单线程
start = time.time()
cpu_bound(50_000_000)
print(f"Single thread: {time.time() - start:.2f}s")

# 双线程（受 GIL 限制）
start = time.time()
t1 = threading.Thread(target=cpu_bound, args=(25_000_000,))
t2 = threading.Thread(target=cpu_bound, args=(25_000_000,))
t1.start(); t2.start(); t1.join(); t2.join()
print(f"Two threads  : {time.time() - start:.2f}s")

import threading, time

def io_task():
    time.sleep(1)  # 模拟 I/O（网络/磁盘），此时 GIL 会释放

# 单线程：4 秒
start = time.time()
for _ in range(4): io_task()
print(f"Single: {time.time()-start:.2f}s")

# 双线程：≈1 秒
start = time.time()
t1 = threading.Thread(target=io_task)
t2 = threading.Thread(target=io_task)
t1.start(); t2.start(); t1.join(); t2.join()
print(f"Two threads: {time.time()-start:.2f}s")

from concurrent.futures import Future
def func(x,y,fut):
    time.sleep(2)
    fut.set_result(x+y)
def caller():
    fut = Future()
    threading.Thread(target=func, args=(2, 3, fut)).start()
    result = fut.result()
    print('Got:', result)
caller()

# Returning Multiple Values
def parse_line(line):
    if '=' not in line:
        return None
    return tuple(line.split('='))
print(parse_line('email=guido@python.org'))
name,val=parse_line('email=guido@python.org')
print(name)
print(val)
print(parse_line('email'))
# Futures
import time
def worker(x,y):
    print('About to work')
    time.sleep(2)
    print('Done')
    return x+y
print(worker(2,3))
import threading
t=threading.Thread(target=worker,args=(2,3))
t.start()
from concurrent.futures import Future
def do_work(x,y,fut):
    fut.set_result(worker(x,y))
fut=Future()
t = threading.Thread(target=do_work, args=(2, 3, fut))
t.start()
result = fut.result()
print(result)