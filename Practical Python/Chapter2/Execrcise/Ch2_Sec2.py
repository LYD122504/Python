#  A list of tuples
import csv
from pprint import pprint
def read_port(filename):
     t_list=[]
     with open(filename,'rt') as f:
         rows=csv.reader(f)
         header=next(rows)
         for row in rows:
             temp=(row[0],int(row[1]),float(row[2]))
             t_list.append(temp)
     return t_list

tl=read_port(r'./portfolio.csv')
print(tl)
print(tl[1])
print(tl[1][2])
total_cost=0.0
for name,share,price in tl:
    total_cost+=share*price
print(total_cost)
pprint(tl)


# List of Dictionaries
def read_dic(filename):
    d_list=[]
    with open(filename,'rt') as f:
        rows=csv.reader(f)
        header=next(rows)
        for row in rows:
            dtemp={}
            dtemp['name']=row[0]
            dtemp['share']=int(row[1])
            dtemp['price']=float(row[2])
            d_list.append(dtemp)
    return d_list
dlist=read_dic(r'./portfolio.csv')
print(dlist)
total_cost=0.0
for dl in dlist:
    total_cost+=dl['share']*dl['price']
print(total_cost)
pprint(dlist)

# Dictionaries as a container
def read_price(filename):
    d={}
    with open(filename,'rt') as f:
        rows=csv.reader(f)
        header=next(rows)
        for row in rows:
            try:
                d[row[0]]=float(row[1])
            except IndexError:
                pass
    return d
dlist=read_price(r'./prices.csv')
pprint(dlist)
print(dlist['IBM'])
print('PB' in dlist)
