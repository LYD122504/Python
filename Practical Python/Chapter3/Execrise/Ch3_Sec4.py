# Exercise 11 Module imports
from Ch3_Sec3 import parse_csv
# help(m.parse_csv)
prices=parse_csv('./data/prices.csv',has_header=True)
print(prices)
# Exercise 12 Using your library module

from pprint import pprint
import csv
# Collecting Data
def read_port(filename):
    return parse_csv(filename,select=['name','shares','price'],type=[str,int,float])

def read_price(filename):
    return dict(parse_csv(filename,has_header=False,type=[str,float]))
def make_report(tlist,dlist):
    newtlist=[]
    for item in tlist:
        o_price=dlist[item['name']]
        t=(item['name'],item['shares'],o_price,o_price-item['price'])
        newtlist.append(t)
    return newtlist
        


port_tl=read_port(r'./data/portfolio.csv')
pprint(port_tl)
price_dl=read_price(r'./data/prices.csv')
pprint(price_dl)
report_tl=make_report(port_tl,price_dl)
headers = ('Name', 'Shares', 'Price', 'Change')
print("%10s %10s %10s %10s"%headers)
s='-'*10
print("%10s %10s %10s %10s"%(s,s,s,s))
for name,share,price,change in report_tl:
    price=f'${price:.2f}'
    print(f'{name:>10s} {share:10d} {price:>10s} {change:10.2f}')

# 3.14 Using more library import
from  report import read_portfolio
def portfolio_cost(filename):
    row=read_portfolio(filename)
    return sum([s['shares']*s['price'] for s in row])
import sys
if len(sys.argv) == 2: # 判断是否有命令行参数
    filename = sys.argv[1]
else:
    filename = input('Enter a filename:')

cost = portfolio_cost(filename)
print('Total cost:', cost)