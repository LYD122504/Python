from pprint import pprint
import csv

value=42863.1
print(value)
print(f'{value:0.4f}')
print(f'{value:>16.2f}')
print(f'{value:<16.2f}')
print(f'{value:*>16.2f}')

print('%0.4f'%value)
print('%16.2f'%value)

v='%0.4f'%value # 利用百分号的格式化字符串赋值
print(v)
# Collecting Data
def read_port(filename):
    tlist=[]
    with open(filename,'rt') as f:
        rows=csv.reader(f)
        header=next(rows)
        for row in rows:
            t=(row[0],int(row[1]),float(row[2]))
            tlist.append(t)
    return tlist

def read_price(filename):
    dlist={}
    with open(filename,'rt') as f:
        rows=csv.reader(f)
        for row in rows:
            try:
                dlist[row[0]]=float(row[1])
            except IndexError:
                pass
    return dlist
def make_report(tlist,dlist):
    newtlist=[]
    for name,share,price in tlist:
        o_price=dlist[name];
        t=(name,share,o_price,o_price-price)
        newtlist.append(t)
    return newtlist
        


port_tl=read_port(r'./portfolio.csv')
pprint(port_tl)
price_dl=read_price(r'./prices.csv')
pprint(price_dl)
report_tl=make_report(port_tl,price_dl)
pprint(report_tl)

for r in report_tl:
    print("%10s %10d %10.2f %10.2f"%r)
    
headers = ('Name', 'Shares', 'Price', 'Change')
print("%10s %10s %10s %10s"%headers)
s='-'*10
print("%10s %10s %10s %10s"%(s,s,s,s))
for name,share,price,change in report_tl:
    price=f'${price:.2f}'
    print(f'{name:>10s} {share:10d} {price:>10s} {change:10.2f}')
