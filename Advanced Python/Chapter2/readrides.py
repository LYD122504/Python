import tracemalloc
from functools import wraps
import typing
import csv
import collections
f=open('../Data/ctabus.csv')
def direct_read():
    data=f.read()
    print(len(data))
    return data
def str_read():
    data=f.readlines()
    print(len(data))
    return data
def tuple_read():
    records=[]
    rows=csv.reader(f)
    headings=next(rows)
    for row in rows:
        records.append((row[0],row[1],row[2],int(row[3])))
    return records
def dict_read():
    records=[]
    rows=csv.reader(f)
    headings=next(rows)
    for row in rows:
        records.append({headings[0]:row[0],headings[1]:row[1],headings[2]:row[2],headings[3]:int(row[3])})
    return records
def dict_readv1():
    records=[]
    rows=csv.DictReader(f)
    for row in rows:
        row['rides']=int(row['rides'])
        records.append(row)
    return records
class Row:
    def __init__(self, route, date, daytype, rides):
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = rides
def class_read():
    records=[]
    rows=csv.reader(f)
    headings=next(rows)
    for row in rows:
        records.append(Row(row[0],row[1],row[2],int(row[3])))
    return records
from collections import namedtuple
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
def slots_read():
    records=[]
    rows=csv.reader(f)
    headings=next(rows)
    for row in rows:
        records.append(Rows(row[0],row[1],row[2],int(row[3])))
    return records
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
class RideData(collections.abc.Sequence):
    def __init__(self):
        self.routes=[]
        self.dates=[]
        self.daytypes=[]
        self.numrides=[]
    def __len__(self):
        return len(self.routes)
    def __getitem__(self,index):
        if isinstance(index,int):
            return {'route': self.routes[index],
                 'date': self.dates[index],
                 'daytype': self.daytypes[index],
                 'rides': self.numrides[index] }
        if isinstance(index,slice):
            result=[]
            routes = self.routes[index]
            dates = self.dates[index]
            daytypes = self.daytypes[index]
            numrides = self.numrides[index]
            for i in range(len(routes)):
                result.append({'route': routes[i],
                 'date': dates[i],
                 'daytype': daytypes[i],
                 'rides': numrides[i] })
            return result
    def append(self,d):
        self.routes.append(d['route'])
        self.dates.append(d['date'])
        self.daytypes.append(d['daytype'])
        self.numrides.append(d['rides'])
def dict_readv2():
    records=RideData()
    rows=csv.reader(f)
    headings=next(rows)
    for row in rows:
        records.append({headings[0]:row[0],headings[1]:row[1],headings[2]:row[2],headings[3]:int(row[3])})
    return records
if __name__ == "__main__":
    '''
    func=[direct_read,str_read,tuple_read,dict_read,dict_readv1,class_read,namedtuple_read,slots_read]
    for fun in func:
        print(f"Running {fun.__name__}")
        fun()
        f.seek(0)
    '''
    records=RideData()