import csv
import reader
from sys import intern
import tracemalloc
import collections
def read_portfolio(filename,type):
    portfolio=[]
    with open(filename) as f:
        rows=csv.reader(f)
        headers=next(rows)
        for row in rows:
            record={name:func(val) for name,func,val in zip(headers,type,row)}
            portfolio.append(record)
    return portfolio
coltypes=[str,int,float]
portfolio=read_portfolio('../Data/portfolio.csv',coltypes)
from pprint import pprint
pprint(portfolio)
portfolio = reader.read_csv_as_dicts('../Data/portfolio.csv', [str,int,float])
for s in portfolio:
    print(s)
tracemalloc.start()
rows = reader.read_csv_as_dicts('../Data/ctabus.csv', [intern,intern,str,int])
#print(len(rows))
#print(rows[0])
#routes={row['route'] for row in rows}
#print(len(routes))
#routeids = { id(row['route']) for row in rows }
#print(len(routeids))
current,peak=tracemalloc.get_traced_memory()
print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")

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
def dict_readv2(filename,types):
    records=RideData()
    with open(filename) as f:
        rows=csv.reader(f)
        headings=next(rows)
        for row in rows:
            records.append({name:func(val) for name,func,val in zip(headings,types,row)})
    return records
data = dict_readv2('../Data/ctabus.csv', types=[str, str, str, int])
print(data)