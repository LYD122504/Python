x=10
a=eval('3*x-2')
print(a)
exec('for i in range(5):print(i)')
def func():
    x=15
    exec('x=10;print(x)')
    print(x)
func()
def foo():
    x=15
    loc=locals()
    exec('x=10;print(x)',globals(),loc)
    x=loc['x']
    print(x)
foo()
# Experiment with exec()
code = '''
for i in range(n):
    print(i, end=' ')
'''
n=10
exec(code)
print()
class Stock:
    _fields=('name','shares','price')
argstr=','.join(Stock._fields)
print(argstr)
code = f'def __init__(self, {argstr}):\n'
for name in Stock._fields:
    code+=f'    self.{name}={name}\n'
print(code)
locs={ }
exec(code,locs)
Stock.__init__=locs['__init__']
s = Stock('GOOG', 100, 490.1)
print(s.name)
print(s.shares)
# Creating an `__init__()` function
from structure import Structure
class Stock(Structure):
    _fields = ('name', 'shares', 'price')
Stock.create_init()
s = Stock(name='GOOG', shares=100, price=490.1)
print(s)
s.shares = 50
# Named Tuples
from collections import namedtuple
Stock=namedtuple('Stock',['name','shares','price'])
s=Stock('GOOG',100,490.1)
print(s.name)
print(s.shares)
print(s[1])
import inspect
print(inspect.getsource(namedtuple))