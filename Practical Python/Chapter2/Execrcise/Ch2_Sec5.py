# Exercise 2.18 Tabulating with Counters
from pprint import pprint
import csv
from collections import Counter
def read_port(filename):
     t_list=[]
     with open(filename,'rt') as f:
         rows=csv.reader(f)
         header=next(rows)
         for row in rows:
             temp=(row[0],int(row[1]),float(row[2]))
             t_list.append(temp)
     return t_list

portfolio=read_port(r'./portfolio.csv')
pprint(portfolio)
holdings=Counter()
for name,share,price in portfolio:
    holdings[name]+=share
pprint(holdings)
print(holdings.most_common(3))

portfolio2=read_port(r'./portfolio2.csv')
pprint(portfolio2)
holdings2=Counter()
for name,share,price in portfolio2:
    holdings2[name]+=share
pprint(holdings2)
print(holdings2.most_common(3))

combined=holdings+holdings2
pprint(combined)