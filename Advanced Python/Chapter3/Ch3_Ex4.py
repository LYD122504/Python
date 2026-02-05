import stock
from decimal import Decimal
class Base:
    def __init__(self,name):
        self._name=name
b=Base('Guido')
print(b._name)
b._name='Dave'
print(b._name)
class Child(Base):
    def spam(self):
        print('Spam', self._name)
c=Child('Dave')
c.spam()
class Stock:
    def __init__(self, name, shares, price):
        self.name = name
        self.shares=shares
        self.price = price
    @property
    def cost(self):
        return self.price*self.shares
    @property
    def shares(self):
        return self._shares
    @shares.setter
    def shares(self,value):
        if isinstance(value,int):
            self._shares=value
        else:
            raise TypeError('Expected int')
s = Stock('GOOG', 100, 490.1)
print(s.shares)
print(s.cost)

row=['GOOG','100','490.1']
s=stock.Stock.from_row(row)
print(s.name)
print(s.shares)
print(s.price)
print(s.cost)
s = stock.Stock('GOOG', 100, 490.10)
s.shares=50
print(s.shares)
s = stock.DStock('AA', 50, Decimal('91.1'))
s.shares=50
print(s.shares)