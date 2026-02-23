def func(a,items=[]):
    items.append(a)
    return items
print(func.__defaults__)
print(func(1))
print(func.__defaults__)
print(func(2))
print(func.__defaults__)
print(func(3))
print(func.__defaults__)
def func(a, items=None):
    if items is None:
        items = []
    items.append(a)
    return items
print(func.__defaults__)
print(func(1))
print(func.__defaults__)
print(func(2))
print(func.__defaults__)
def foo(name=None):
    if name is not None:
        print('Hello',name)
foo()
foo("Guido")
import reader
from pprint import pprint
from stock import Stock
port=reader.read_csv_as_dicts('../Data/portfolio.csv',[str,int,float])
pprint(port)
inport=reader.read_csv_as_instances('../Data/portfolio.csv',Stock)
pprint(inport)
import gzip
file=gzip.open('../Data/portfolio.csv.gz','rt')
ports=reader.csv_as_instances(file,Stock)
pprint(ports)
headers=['name','price','shares']
ports=reader.read_csv_as_dicts('../Data/portfolio_noheader.csv',[str,int,float],headers=headers)
pprint(ports)
def add(x:int,y:int) -> int:
    return x+y
from typing import List
def sum_squares(nums:List[int]) ->int:
    total =0
    for n in nums:
        total+=n*n
    return total