# Positional Variable-Length Arguments
def f(x,*args):
    print("x =", x)
    print("args =", args)
    print(type(args))
f(1,2,3,4)
f(1)
# Keyword Variable-Length Arguments
def g(x,t,**kwargs):
    print("x =", x)
    print("t =", t)
    print("kwargs =", kwargs)
    print(type(kwargs))
g(2,3,flag=True,mode='fast',header='debug')
g(5,6)
# Both
def f(*args,**kwargs):
    print("args =", args)
    print("kwargs =", kwargs)
f(1,2,3,flag=True,mode='fast')
f()
# Passing Tuples and Dicts
numbers=(1,2,3,4)
f(*numbers)
options={'flag':True,'mode':'fast'}
f(**options)