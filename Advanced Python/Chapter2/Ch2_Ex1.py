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
def direct_read():
    data=f.read()
    print(len(data))
    return data
@memory
def str_read():
    data=f.readlines()
    print(len(data))
    return data
@memory
def tuple_read():
    records=[]
    rows=csv.reader(f)
    headings=next(rows)
    for row in rows:
        records.append((row[0],row[1],row[2],int(row[3])))
    return records
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
class Stock(typing.TypedDict):
    route: str
    date: str
    daytype: str
    rides: int
class Row:
    def __init__(self, route, date, daytype, rides):
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = rides

@memory
def class_read():
    records=[]
    rows=csv.reader(f)
    headings=next(rows)
    for row in rows:
        records.append(Row(row[0],row[1],row[2],int(row[3])))
    return records
from collections import namedtuple
@memory
def namedtuple_read():
    records=[]
    Row=namedtuple('Row',['route','date','daytype','rides'])
    rows=csv.reader(f)
    headings=next(rows)
    for row in rows:
        records.append(Row(row[0],row[1],row[2],int(row[3])))
    return records
class Rows:
    __slots__ = ['route', 'date', 'daytype', 'rides']
    def __init__(self, route, date, daytype, rides):
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = rides
@memory  
def slots_read():
    records=[]
    rows=csv.reader(f)
    headings=next(rows)
    for row in rows:
        records.append(Rows(row[0],row[1],row[2],int(row[3])))
    return records
if __name__ == "__main__":
    tracemalloc.start()
    snapshot1 = tracemalloc.take_snapshot()
    # 执行一些操作
    my_list = [i for i in range(10000)]
    snapshot2 = tracemalloc.take_snapshot()
    top_stats = snapshot2.compare_to(snapshot1, 'lineno')  # 比较内存变化
    for stat in top_stats[:10]:
        print(stat)
    tracemalloc.stop()
    func=[direct_read,str_read,tuple_read,dict_read,dict_readv1,class_read,namedtuple_read,slots_read]
    for fun in func:
        print(f"Running {fun.__name__}")
        fun()
        f.seek(0)