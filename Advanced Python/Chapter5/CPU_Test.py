import time
from multiprocessing import Process, Value

def cpu_bound(n, counter):
    """纯 CPU 密集型任务"""
    while n > 0:
        n -= 1
        counter.value += 1

if __name__ == '__main__':  # ⚠️ Windows 必须加此保护
    # ========== 单进程测试 ==========
    counter1 = Value('i', 0)  # 共享整数
    start = time.time()
    cpu_bound(500000, counter1)
    print(f"Single process: {time.time() - start:.2f}s, count={counter1.value}")

    # ========== 双进程测试（真正并行） ==========
    counter2 = Value('i', 0)
    counter3 = Value('i', 0)
    start = time.time()
    
    p1 = Process(target=cpu_bound, args=(250000, counter2))
    p2 = Process(target=cpu_bound, args=(250000, counter3))
    
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    
    total = counter2.value + counter3.value
    print(f"Two processes : {time.time() - start:.2f}s, count={total}")