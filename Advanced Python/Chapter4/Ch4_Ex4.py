class Demo:
    def __init__(self):
        self.existing = 'I exist'
    def __getattribute__(self, name):
        print(f'__getattribute__ 被调用: "{name}"')
        try:
            return super().__getattribute__(name)
        except AttributeError:
            print(f"标准查找失败,需要触发getattr")
            raise
    def __getattr__(self,name):
        print(f"__getattr__ 被调用（后备）: '{name}'")
        return f"默认值: {name}"
obj=Demo()
print("\n--- 访问存在的属性 ---")
print(obj.existing)

print("\n--- 访问不存在的属性 ---")
print(obj.missing)
# Proxy
class Proxy:
    def __init__(self,obj):
        self._obj=obj
    def __getattr__(self,name):
        print("getattr: ",name)
        return getattr(self._obj,name)
class Circle:
    def __init__(self,rad):
        self.radius=rad
    def area(self):
        import math
        return math.pi*self.radius**2
c=Circle(4.0)
print(c.radius)
print(c.area())
p=Proxy(c)
print(p)
print(p.radius)
print(p.area())
# Delegation
class A:
    def foo(self):
        print('A.foo')
    def bar(self):
        print('A.bar')
class B:
    def __init__(self):
        self._a=A()
    def bar(self):
        print('B.bar')
        self._a.bar()
    def __getattr__(self,name):
        return getattr(self._a,name)
b=B()
b.foo()
b.bar()
class Wrapper:
    def __init__(self, obj):
        self._obj = obj
    
    def __getattr__(self, name):
        print(f"__getattr__ called for: {name}")
        return getattr(self._obj, name)

# 被包装的对象
class Inner:
    def __init__(self):
        self.normal_attr = "normal"
    
    def __len__(self):
        return 42
    
    def regular_method(self):
        return "hello"

w = Wrapper(Inner())

# 普通属性/方法 → ✅ 触发 __getattr__
print(w.normal_attr)      # __getattr__ called for: normal_attr → "normal"
print(w.regular_method()) # __getattr__ called for: regular_method → "hello"
# TypeError: object of type 'Wrapper' has no len()
# slots vs setattr
class Stock:
    def __init__(self,name,shares,price):
        self.name=name
        self.shares=shares
        self.price=price
    def __setattr__(self,name,value):
        if name not in {'name','shares','price'}:
            raise AttributeError('No attribute %s' % name)
        super().__setattr__(name,value)
s=Stock('GOOG',100,490.10)
print(s.name)
s.shares=75
print(s.shares)
# Proxy
class Readonly:
    def __init__(self,obj):
        self.__dict__['_obj']=obj
    def __setattr__(self, name, value):
        raise AttributeError("Can't set attribute")
    def __getattr__(self,name):
        return getattr(self._obj,name)
from stock import Stock
s=Stock('GOOG',100,490.10)
p=Readonly(s)
print(p.name)
print(p.shares)
print(p.cost())
# Delegation as an alternative to inheritance
class Spam:
    def a(self):
        print('Spam.a')
    def b(self):
        print('Spam.b')
class MySpam:
    def __init__(self):
        self._spam=Spam()
    def a(self):
        print('MySpam.a')
        self._spam.a()
    def c(self):
        print('MySpam.c')
    def __getattr__(self,name):
        return getattr(self._spam,name)
s=MySpam()
s.a()
s.b()
s.c()