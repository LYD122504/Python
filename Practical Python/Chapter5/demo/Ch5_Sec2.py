import logging
from functools import wraps
class Person(object):
    def __init__(self,name):
        self._name=name

p=Person('Guido')
print(p._name)
p._name='Dave'
print(p._name)

class Stock:
    def __init__(self, name, shares, price):
        self.name = name
        self.set_shares(shares)
        self.price = price
    def get_shares(self):
        return self._shares
    def set_shares(self,value):
        if not isinstance(value,int):
            raise TypeError("Expected an int")
        self._shares=value
'''s=Stock('IBM',50,91.1)
print(s.shares)
s.shares="hundred"
print(s.shares)
s.shares=[1,0,0]
print(s.shares)'''

class Stock:
    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

    @property
    def shares(self):
        return self._shares

    @shares.setter
    def shares(self, value):
        if not isinstance(value, int):
            raise TypeError('Expected int')
        self._shares = value

print(Stock.__dict__)
print(Stock.__dict__['shares'])

logging.basicConfig(level=logging.INFO)
def foo():
    print('i am foo')
    logging.info("foo is running")
foo()
def use_logging(func):
    logging.info("%s is running" % func.__name__)
    func()
def bar():
    print('i am bar')
use_logging(bar)

def use_logging(func):
    def wrapper(*args,**kwargs):# 保证被装饰函数 func 可以是任意参数形式
        logging.info("%s is running" % func.__name__)
        return func(*args,**kwargs)
    return wrapper
bars=use_logging(bar)
print(bars.__name__)
bars()

def foo(x):
    return x+1
foo=use_logging(foo)
print(foo(1))
@use_logging
def bar():
    print('i am bar')
bar()
print(bar.__name__)
def use_logging(level):
    def decorator(func):
        def wrapper(*args,**kwargs):# 保证被装饰函数 func 可以是任意参数形式
            if level=='info':
                logging.info("%s is running" % func.__name__)
            return func(*args,**kwargs)
        return wrapper
    return decorator
@use_logging('info')
def bar():
    print('i am bar')
bar()

class Foo(object):
    def __init__(self,func):
        self._func=func
    def __call__(self):
        print('class decorator running')
        self._func()
        print('class decorator ending')
@Foo
def bar():
    print('bar')
bar()
print(type(bar))

def logged(func):
    @wraps(func)
    def with_logging(*args,**kwargs):
        print(func.__name__+' was called')
        return func(*args,**kwargs)
    return with_logging
@logged
def f(x):
    '''does some math'''
    return x+x*x
print(f.__name__)
print(f.__doc__)

class Stock:
    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

    @property
    def cost(self):
        return self.shares * self.price
s=Stock('GOOG', 100, 490.1)
print(s.shares)
print(s.cost)
print(Stock.__dict__['cost'])