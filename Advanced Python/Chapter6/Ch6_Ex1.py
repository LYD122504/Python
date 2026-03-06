def func(x,*args):
    print(x)
    print(args)
func(1,2,3,4)
arg=(2,3,4)
func(1,*arg)
def foo(x,y,**kwargs):
    print(x)
    print(y)
    print(kwargs)
foo(2,3,flag=True,mode='fast',header="debug")
kwargs = {
    'color': 'red', 'delimiter': ',',
    'width': 400
}
foo(2,3, **kwargs)
def foo(x,y,z):
    return x+y+z
print(foo(1,2,3))
print(foo(1,z=3,y=2))
args=(1,3,4)
print(foo(*args))
kwargs={'y':4,'z':3}
print(foo(1,**kwargs))
def foo(*args):
    print(args)
foo(1,2)
foo(1,2,3,4,5)
foo()
def bar(**kwargs):
    print(kwargs)
bar(x=1,y=2)
bar(x=2,z=3,y=1)
bar()
# Simplified Data Structures
import stock
s = stock.Stock('GOOG',100,490.1)
s1=stock.Date(2026,2,14)
print(s.__class__.__name__)
print(s.name)
print(s.shares)
print(s.price)
print(repr(s))
print(repr(s1))
s._shares=50