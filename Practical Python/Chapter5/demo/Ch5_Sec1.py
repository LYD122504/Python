# Practical Python
class Stock:
    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

    def cost(self):
        return self.shares * self.price

    def sell(self, nshares):
        self.shares -= nshares
s = Stock('GOOG', 100, 490.1)     # {'name' : 'GOOG','shares' : 100, 'price': 490.1 }
t = Stock('AAPL', 50, 123.45)
print(s.__dict__)
print(t.__dict__)
print(Stock.__dict__)

class A:
    x=1
    def func(self):
        return A.x
a=A()
a.y=2
a.foo = 123
a.bar = lambda x: x + 1
a.anything = "whatever"
print(a.__dict__)
print(A.__dict__)

def getarr(obj, name):
    cls = obj.__class__

    # 1️⃣ 查找 data descriptor（类 & MRO）
    for base in cls.__mro__:
        if name in base.__dict__:
            attr = base.__dict__[name]
            if is_data_descriptor(attr):
                return attr.__get__(obj, cls)

    # 2️⃣ 查实例字典
    if name in obj.__dict__:
        return obj.__dict__[name]

    # 3️⃣ 查 non-data descriptor 或普通类属性
    for base in cls.__mro__:
        if name in base.__dict__:
            attr = base.__dict__[name]
            if hasattr(attr, "__get__"):
                return attr.__get__(obj, cls)
            return attr

    raise AttributeError(name)
def is_data_descriptor(attr):
    return hasattr(attr, "__set__") or hasattr(attr, "__delete__")

def is_non_data_descriptor(attr):
    return hasattr(attr, "__get__")
# 实例属性
class A:
    x = 1
a = A()
a.x = 100     # 实例属性，遮蔽类属性
print(getarr(a, 'x'))   # 100
# 类属性
b= A()
print(getarr(b, 'x'))   # 1
# 单继承父类属性
class Base:
    x = 10
class A(Base):
    pass
a = A()
print(getarr(a, 'x'))   # 10
# 多重继承
class B:
    x = 2
class C:
    x = 3
class A(B, C):
    pass
a = A()
print(A.__mro__)
print(getarr(a, 'x'))   # 2
# 异常
class A:
    pass
a = A()
try:
    getarr(a, 'not_exist')
except AttributeError as e:
    print("AttributeError:", e)

# method
class A:
    def foo(self,x):
        return x+1
a=A()
try:
    f=getarr(a, 'foo')
    print(f(10))
except AttributeError as e:
    print("AttributeError:", e)

print(globals())


class A:
    def func(self):
        return 1
print(A.__dict__['func'])
print(A.__dict__['func'].__get__(a, A))


class A:
    def f(self):
        return "method called"
a=A()
# a.f调用function的 __get__,返回bound method
print(a.f())   # "method called"
# 实例属性遮蔽non-datadescriptor
a.f = "instance attribute"
print(a.f)     # "instance attribute"(覆盖了 class的f)

class B:
    def __init__(self):
        self._x=10
    @property
    def x(self):
        return self._x
b=B()
print(b.x) # 10

b.__dict__['x'] = 999
print(b.x)  # 10 （data descriptor 优先，实例字典被遮蔽）

class A:
    def f(self):
        return 1
a=A()
a.x=1
print(A.__dict__['f']) # function 对象
print(A.__dict__['f'].__get__(a,A)) # bound method
print(A.__dict__['__dict__'].__get__(a, A))
print(A.__dict__['__dict__'])
print(A.__dict__['__dict__'].__get__(a,A))




class A:
    def f(self):
        return "method"

a = A()
a.f = "instance attr"

print(getarr(a, "f"))
# instance attr

class B:
    def __init__(self):
        self._x = 1

    @property
    def x(self):
        return self._x

b = B()
b.__dict__["x"] = 999

print(getarr(b, "x"))
# 1

class A:
    __slots__ = ('x',)

print(A.__dict__)
print('__dict__' in A.__dict__)   # False
print('x' in A.__dict__)          # True
a=A()
print(a.__slots__)