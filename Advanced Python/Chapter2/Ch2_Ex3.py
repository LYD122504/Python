'''
prices = [
    ['GOOG', 490.1, 485.25, 487.5 ],
    ['IBM', 91.5],
    ['HPE', 13.75, 12.1, 13.25, 14.2, 13.5 ],
    ['CAT', 52.5, 51.2]
    ]
for name,*price in prices:
    print(name,'->',price)

# Unpacking in lists and tuples
a=(1,2,3)
b=[4,5]
c=[*a,*b]
d=(*a,*b)
print(c)
print(d)

# Unpacking Dictionaries
a={ 'name': 'GOOG', 'shares': 100, 'price':490.1 }
b = { 'date': '6/11/2007', 'time': '9:45am' }
c = { **a, **b }
print(c)

# Exercise 2.3
import csv
f=open('../Data/portfolio.csv')
f_csv=csv.reader(f)
headers=next(f_csv)
print(headers)
rows=list(f_csv)
from pprint import pprint
pprint(rows)
for row in rows:
    print(row)
for name,shares,price in rows:
    print(f'Name: {name}, Shares: {shares}, Price: {price}')
for name,_,price in rows:
    print(f'Name: {name}, Price: {price}')
from collections import defaultdict
byname=defaultdict(list)
for name,*values in rows:
    byname[name].append(values)
print(byname['IBM'])
for shares, price in byname['IBM']:
    print(shares, price)

# Counting with enumerate()
for rowno,row in enumerate(rows):
    print(f'Row {rowno}: {row}')
for rowno, (name, shares, price) in enumerate(rows):
    print(rowno, name, shares, price)

# Using the zip() function
row=rows[0]
for col,val in zip(headers,row):
    print(f'{col}: {val}')
dict_row=dict(zip(headers,row))
print(dict_row)

# Generator Expressions
nums=[1,2,3,4,5]
squares=(x*x for x in nums)
print(squares)
for n in squares:
    print(n)
squares=(x*x for x in nums)
print(next(squares))
print(next(squares))
print(next(squares))
def squares(nums):
    for x in nums:
        yield x*x
for n in squares([1,2,3,4,5]):
    print(n)

# Generator Expressions and Reduction Functions
from readport import read_portfolio
portfolio=read_portfolio('../Data/portfolio.csv')
print(sum(s['shares']*s['price'] for s in portfolio))
print(min(s['shares'] for s in portfolio))
print(any(s['name']=='IBM' for s in portfolio))
print(all(s['name'] == 'IBM' for s in portfolio))
print(sum(s['shares'] for s in portfolio if s['name'] == 'IBM'))
s=('GOOG',100,490.10)
print(','.join(str(x) for x in s))

# Saving a lot of memory
import tracemalloc
tracemalloc.start()
import readrides
rows=readrides.dict_read()
rt22=[row for row in rows if row['route']=='22']
print(max(rt22,key=lambda r:r['rides']))
current,peak=tracemalloc.get_traced_memory()
print(f'Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB')
tracemalloc.stop()
tracemalloc.start()
import csv
f=open('../Data/ctabus.csv')
f_csv=csv.reader(f)
heading=next(f_csv)
rows=(dict(zip(heading,row)) for row in f_csv)
rt22=(row for row in rows if row['route']=='22')
print(max(rt22,key=lambda r:int(r['rides'])))
current,peak=tracemalloc.get_traced_memory()
print(f'Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB')
tracemalloc.stop()
'''
# __slot__
class A:
    __slots__ = ('b',)
class B(A):
    __slots__ = ('b',)
obj=B()
print(B.__dict__)
# dataclass
from dataclasses import dataclass
@dataclass
class Person:
    name: str
    age: int
p = Person("Alice", "30")  # age 其实是 str，但 Python 不会报错
print(p)