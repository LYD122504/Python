class Spam(metaclass=type):
    def __init__(self,name):
        self.name=name
    def yow(self):
        print("Yow!",self.name)
s=Spam('Test')
s.yow()
class mytype(type):
    @staticmethod
    def __new__(meta,name,bases,methods):
        print('Creating class:',name)
        print('Base classes:',bases)
        print('Methods:',list(methods))
        return super().__new__(meta,name,bases,methods)
    
class myobject(metaclass=mytype):
    pass
class Spam(myobject):
    def __init__(self, name):
        self.name = name
    def yow(self):
        print("Yow!", self.name)
from mymeta import myobject
class Stock(myobject):
    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price
    def cost(self):
        return self.shares * self.price
    def sell(self, nshares):
        self.shares -= nshares
s=Stock('GOOG',100,490.1)
class MyStock(Stock):
    pass