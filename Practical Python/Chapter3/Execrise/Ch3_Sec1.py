from pprint import pprint
import csv
def read_portfolio(filename):
    '''
    Read a stock portfolio file into a list of dictionaries with keys name, shares, and price.
    '''
    portfolio=[]
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

def print_report(re_list):
    headers = ('Name', 'Shares', 'Price', 'Change')
    print("%10s %10s %10s %10s"%headers)
    print(('-' * 10 + ' ') * len(headers))
    for row in re_list:
        print('%10s %10d %10.2f %10.2f' % row)
        # Ex1
'''
port_tl=read_port(r'./portfolio.csv')
price_dl=read_price(r'./prices.csv')
report_tl=make_report(port_tl,price_dl)
print_report(report_tl)
'''
# Ex2
def portfolio_report(filename1,filename2):
    p_list=read_port(filename1)
    price_list=read_price(filename2)
    report_list=make_report(p_list,price_list)
    print_report(report_list)
    
portfolio_report('./portfolio.csv','prices.csv')
files=['portfolio.csv','portfolio2.csv']
for name in files:
    print(f'{name:-^43s}')#用-填充并且居中展示
    portfolio_report(name, 'prices.csv')
    print()
