class Callable:
    def __call__(self, *args, **kwargs):
        print('Calling',args,kwargs)
c=Callable()
c(2,3,color='red')
class Memoize:
    def __init__(self,func):
        self._cache={}
        self._func=func
    def __call__(self,*args):
        if args in self._cache:
            return self._cache[args]
        r=self._func(*args)
        self._cache[args]=r
        return r
    def clear(self):
        self._cache.clear()
@Memoize  # 等同于 fib = Memoize(fib)
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)
# 调用时完全像普通函数
print(fib(10)) 
fib.clear()  # 清除缓存，这是普通函数做不到的
from validate import Integer,ValidatedFunction
print(Integer.check(1))
def add(x,y):
    Integer.check(x)
    Integer.check(y)
    return x+y
# Creating a Callable Object
def add(x: Integer,y: Integer):
    return x+y
add=ValidatedFunction(add)
print(add(2,3))
# Enforcement
# print(add('two','three'))
# Use as a Method
import stock
s = stock.Stock('GOOG', 100, 490.1)