import csv
from validate import String,PositiveInteger,PositiveFloat
from decimal import Decimal
class DeStock:
    name=String()
    shares=PositiveInteger()
    price=PositiveFloat()
    def __init__(self,name,shares,price):
        self.name=name
        self.shares=shares
        self.price=price
class Stock:
    __slots__=['name','_shares','_price']
    _types=(str,int,float)
    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price
    def cost(self):
        return self.shares * self.price
    @property
    def shares(self):
        return self._shares
    @shares.setter
    def shares(self,value):
        self._shares = PositiveInteger.check(value)
    @property
    def price(self):
        return self._price
    @price.setter
    def price(self,value):
        if not isinstance(value, self._types[2]):
            raise TypeError(f'Expected {self._types[2]}')
        if value < 0:
            raise ValueError('shares must be >= 0')
        self._price = value    
    def sell(self,num):
        self.shares-=num
    @classmethod
    def from_row(cls,row):
        values=[func(val) for func,val in zip(cls._types,row)]
        return cls(*values)
    def __repr__(self):
        return ("Stock('%s',%s,%s)" % (self.name,self.shares,self.price))
    def __eq__(self,other):
        return isinstance(other,Stock) and (self.name,self.shares,self.price)==(other.name,other.shares,other.price)
class DStock(Stock):
    _types=(str,int,Decimal)
def read_portfolio(filename):
    records=[]
    with open(filename) as f:
        rows=csv.reader(f)
        headings=next(rows)
        for row in rows:
            record=Stock(str(row[0]),int(row[1]),float(row[2]))
            records.append(record)
        return records
def print_portfolio(portfolio):
    headings=['name','shares','prices']
    print(f'{headings[0]:>10} {headings[1]:>10} {headings[2]:>10}')
    for i in range(3):
        print('-'*10,end=' ')
    print()
    for s in portfolio:
        print('%10s %10d %10.2f' % (s.name, s.shares, s.price))
if __name__ == "__main__":
    s=Stock('GOOG',100,490.1)
    print(s.name)
    print(s.shares)
    print(s.price)
    s.sell(25)
    print(s.shares)
    portfolio=read_portfolio('../Data/portfolio.csv')
    print_portfolio(portfolio)