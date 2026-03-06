x=43
print(type(x))
s='Hello'
print(type(s))
items=[1,2,3]
print(type(items))
a=list()
print(a)
b=tuple(items)
print(b)
class Spam:
    pass
s=Spam()
print(type(s))
print(type(Spam))
print(isinstance(Spam,type))
class Spam(object):
    def __init__(self,name):
        self.name=name
    def yow(self):
        print("Yow!",self.name)
s=Spam('Test')
s.yow()
# Define some method functions
def __init__(self,name):
    self.name=name
def yow(self):
    print("Yow!",self.name)
# Make a method table
methods={'__init__':__init__,'yow':yow}
# Make a new type
Foo=type('Foo',(object,),methods)
f=Foo('Test')
f.yow()
body='''
def __init__(self,name):
    self.name=name
def yow(self):
    print("Yow!",self.name)
'''
__dict__=type.__prepare__('Spam',(object,))
print(__dict__)
__dict__['__qualname__'] = 'Spam'
__dict__['__module__'] = 'modulename'
exec(body,globals(),__dict__)
print(__dict__)
Spam = type('Spam', (object,), __dict__)
print(Spam)
# Class creation
class Stock:
    def __init__(self,name,shares,price):
        self.name=name
        self.shares=shares
        self.price=price
    def cost(self):
        return self.shares*self.price
    def sell(self,nshares):
        self.shares-=nshares
def __init__(self,name,shares,price):
    self.name=name
    self.shares=shares
    self.price=price
def cost(self):
    return self.shares*self.price
def sell(self,nshares):
    self.shares-=nshares
methods={'__init__':__init__,'cost':cost,'sell':sell}
Stock=type('GOOG',(object,),methods)
s=Stock('AA',100,91.1)
print(s)
print(s.name)
print(s.cost())
s.sell(25)
print(s.shares)
# Typed structures
from validate import String,PositiveInteger,PositiveFloat
from structure import typed_structure
Stock=typed_structure('Stock',name=String(),shares=PositiveInteger(),price=PositiveFloat())
s=Stock('GOOG',100,490.1)
print(s.name)