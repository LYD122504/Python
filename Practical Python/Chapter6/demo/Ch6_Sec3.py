# Producer
def follow(f):
    """生产者，从文件中逐行读取数据"""
    while True:
        line = f.readline()
        if not line:
            break
        yield line  # 生产数据
with open("../data/portfolio.csv") as f:
    for line in follow(f):  # 消费数据
        print(line.strip())

# Producer
def producer():
    for i in range(10):
        yield i  # 生成 0~9 的整数
# Processing stage: square the number
def square(numbers):
    for n in numbers:
        yield n ** 2  # 消费并生成新的数据
# Processing stage: filter even numbers
def even_filter(numbers):
    for n in numbers:
        if n % 2 == 0:
            yield n  # 只输出偶数
# Consumer
def consumer(numbers):
    for n in numbers:
        print("Consumed:", n)
# 设置流水线
a = producer()
b = square(a)
c = even_filter(b)
consumer(c)