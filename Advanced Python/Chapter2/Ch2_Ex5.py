import sys
# list over-allocation
'''
a=[]
print(sys.getsizeof(a))
for i in range(10):
    a.append(i)
    print(a,sys.getsizeof(a))
'''
import sys

def test_set_memory():
    print(f"{'元素数量':>8} {'内存(字节)':>10} {'是否扩容?':>10}")
    print("-" * 30)
    
    a = set()
    prev_size = sys.getsizeof(a)
    print(f"{len(a):>8} {prev_size:>10} {'初始':>10}")
    
    for i in range(30):  # 添加 0 到 29
        a.add(i)
        curr_size = sys.getsizeof(a)
        is_resize = "是" if curr_size != prev_size else "否"
        print(f"{len(a):>8} {curr_size:>10} {is_resize:>10}")
        prev_size = curr_size

print("Python 版本:", sys.version)
test_set_memory()

# set over-allocation
a=set()
print(sys.getsizeof(a))
for i in range(20):
    a.add(i)
    print(a,sys.getsizeof(a))
# dict over-allocation
a={}
print(sys.getsizeof(a))
for i in range(20):
    a[i]=i+1
    print(a,sys.getsizeof(a))
print(16/3*2)
# Hashing
a='Python'
b='Guido'
c='Dave'
d='Test'
print(a.__hash__())
print(b.__hash__())
print(c.__hash__())

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash((self.x, self.y))  # 基于值计算哈希

# 注意：没有定义 __eq__！

p1 = Point(1, 2)
p2 = Point(1, 2)

print(hash(p1) == hash(p2))  # True ✅
print(p1 == p2)              # False ❌（因为默认是 p1 is p2）
print(p1 is p2)              # False

# 放入 set
s = {p1, p2}
print(len(s))  # 输出: 2 ❌（你可能期望是 1！）

hash_list=[0]*8
print(hash_list)
entries=[a,b,c,d]
hash_index=[a.__hash__(),b.__hash__(),c.__hash__(),d.__hash__()]
def perturb(h,size):
    assert size&(size+1)==0
    i=h&size
    per=h
    while True:
        yield i
        i = (i * 5 + per + 1) & size
        per >>= 5

for i in hash_index:
    size=len(hash_list)-1
    if hash_list[i&size]==0:
        hash_list[i&size]=entries[hash_index.index(i)]
    else:
        gen=perturb(i&size,size)
        while True:
            n=next(gen)
            if hash_list[n]!=0:
                continue
            else:
                hash_list[n]=entries[hash_index.index(i)]
                print(n)
                break
        print('error',i,hash_index.index(i))

print(hash_list)

# Ex List Growth
import tracemalloc
from functools import wraps
import typing
import csv
f=open('../Data/ctabus.csv')
def memory(func):
    @wraps(func)
    def wrapper():
        tracemalloc.start()
        record=func()
        current, peak = tracemalloc.get_traced_memory()
        print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
        #total=tracemalloc.take_snapshot()
        #print(total.statistics('lineno')[:3])
        tracemalloc.stop()
    return wrapper
@memory
def dict_read():
    records=[]
    rows=csv.reader(f)
    headings=next(rows)
    for row in rows:
        records.append({headings[0]:row[0],headings[1]:row[1],headings[2]:row[2],headings[3]:int(row[3])})
    return records
@memory
def dict_readv1():
    records=[]
    rows=csv.DictReader(f)
    for row in rows:
        row['rides']=int(row['rides'])
        records.append(row)
    return records
@memory
def columns_read():
    routes=[]
    dates=[]
    daytypes=[]
    numrides=[]
    rows=csv.reader(f)
    headings=next(rows)
    for row in rows:
        routes.append(row[0])
        dates.append(row[1])
        daytypes.append(row[2])
        numrides.append(int(row[3]))
    return dict(routes=routes, dates=dates, daytypes=daytypes, numrides=numrides)
func=[dict_read,dict_readv1,columns_read]
for fun in func:
    print(f"Running {fun.__name__}")
    fun()
    f.seek(0)
import readrides
rows=readrides.dict_readv2()
print(rows[0:10])
