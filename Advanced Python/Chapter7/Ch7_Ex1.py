def add(x,y):
    return x+y
def logged_add(x,y):
    print('Calling add')
    return add(x,y)
print(add(3,4))
print(logged_add(3,4))
def logged(func):
    def wrapper(*args,**kwargs):
        print('Calling',func.__name__)
        return func(*args,**kwargs)
    return wrapper
log_add=logged(add)
print(log_add)
print(log_add(3,4))
@logged
def add(x,y):
    return x+y
print(add(3,4))
import time
def timethis(func):
    def wrapper(*args,**kwargs):
        start=time.time()
        r=func(*args,**kwargs)
        end=time.time()
        print(func.__name__, end - start)
        return r
    return wrapper
@timethis
def bigcalculation():
    n=10000
    res=0
    for i in range(n):
        res+=i
    return res
print(bigcalculation())
# Your First Decorator
import sample
print(sample.add(3,4))
print(sample.sub(7,2))
# A Real Decorator
from validate import Integer, PositiveInteger,validated

@validated
def add(x: Integer, y:Integer) -> Integer:
    return x + y

@validated
def pow(x: Integer, y:PositiveInteger) -> Integer:
    return x ** y
print(add(2,3))
print(pow(2, 3))
