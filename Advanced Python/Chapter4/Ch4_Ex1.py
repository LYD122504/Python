class Stock:
    def __init__(self,name,shares,price):
        self.name=name
        self.shares=shares
        self.price=price
    def cost(self):
        return self.price*self.shares
    def sell(self,nshares):
        self.shares-=nshares
print(Stock.__dict__)
s=Stock('GOOG',100,490.10)
print(s.__dict__)
print(s.__class__)

class SimpleStock:
    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price
    def cost(self):
        return self.shares * self.price
goog=SimpleStock('GOOG',100,490.10)
ibm=SimpleStock('IBM',50,91.23)
# Representation of Instances
print(goog.__dict__)
print(ibm.__dict__)
# Modification of Instance Data
goog.date='6/2/2026'
print(goog.__dict__)
print(ibm.__dict__)
goog.__dict__['time']='9:45am'
print(goog.time)
# The role of classes
print(goog.__class__)
print(ibm.__class__)
print(goog.cost())
print(ibm.cost())
print(SimpleStock.__dict__['cost'])
print(SimpleStock.__dict__['cost'](goog))
print(SimpleStock.__dict__['cost'](ibm))
SimpleStock.spam = 42
print(ibm.spam)
print(goog.spam)
print(ibm.__dict__)
print(SimpleStock.__dict__['spam'])