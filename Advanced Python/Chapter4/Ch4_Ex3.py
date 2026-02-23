class Descriptor:
    def __init__(self,name):
        self.name=name
    def __get__(self,instance,cls=None):
        print('%s:__get__' % self.name)
        return instance.__dict__[self.name]
    def __set__(self,instance,value):
        print('%s:__set__ %s' % (self.name, value))
        instance.__dict__[self.name]=value
    def __delete__(self,instance):
        print('%s:__delete__' % self.name)
class Foo:
    a=Descriptor('A')
    b=Descriptor('B')
f=Foo()
f.a=42
print(f.a)
print(f.__dict__['A'])
print(f.__dict__)
f.a
import stock
s=stock.Stock('GOOG',100,490.10)
# class attribute lookup
value=stock.Stock.__dict__['cost']
print(value)
#descriptor check
print(hasattr(value,'__get__'))
print(hasattr(value,'__set__'))
print(hasattr(value,'__delete__'))
#invocation
result=value.__get__(s,stock.Stock)
print(result)
print(result())
p=stock.Stock.__dict__['shares']
print(p)
p.__set__(s,100)# same as s.shares=100
print(p.__get__(s,stock.Stock)) # same as s.shares
print(s.shares)
class Foo:
    __slots__=('x','y','z')
import numbers
class Integer:
    def __init__(self,name):
        self.name='_'+name
    def __set__(self,instance,value):
        if not isinstance(value,int):
            raise TypeError('Expected an integer')
        instance.__dict__[self.name]=value
class String:
    def __init__(self,name,maxlen):
        self.name=name
        self.maxlen=maxlen
    def __get__(self,instance,cls):
        return instance.__dict__[self.name]
    def __set__(self,instance,value):
        if not isinstance(value,str):
            raise TypeError('Expected a string')
        if len(value)>self.maxlen:
            raise TypeError('The length must be less than 8')
        instance.__dict__[self.name]=value
class Real:
    def __init__(self,name):
        self.name=name
    def __get__(self,instance,cls):
        return instance.__dict__[self.name]
    def __set__(self,instance,value):
        if not isinstance(value,(int,float)):
            raise TypeError('Expected an integer or float')
        if not isinstance(value,numbers.Real):
            raise TypeError('The number must be real')
        instance.__dict__[self.name]=value
class Stock:
    name=String('name',maxlen=8)
    shares=Integer('shares')
    price=Real('price')
s=Stock()
s.name='Hello'
s.shares=10
print(s._shares)
print(s.name)

class Descriptorv1:
    def __init__(self,name):
        self.name=name
    def __get__(self, instance, cls):
        if instance is None:
            # If no instance given, return the descriptor
            # object itself
            return self
        else:
        # Return the instance value 
            return instance.__dict__[self.name]
    def __set__(self,instance,value):
        print('%s:__set__ %s' % (self.name, value))
        instance.__dict__[self.name]=value
class Foo:
    a=Descriptorv1('A')
    b=Descriptorv1('B')
f=Foo()
f.a=42
print(f.a)
print(f.__dict__['A'])
print(f.__dict__)
print(Foo.a)
class MethodDescriptor:
    def __get__(self,instance,cls):
        print('Getting')
class Foo(object):
    a=MethodDescriptor()
f=Foo()
Foo.a
class Descriptor:
    def __init__(self, name=None):
        self.name = name
    def __get__(self, instance, cls):
        return instance.__dict__[self.name]
    def __set_name__(self, cls, name):
        self.name=name
    def __set__(self,instance,value):
        instance.__dict__[self.name]=value 
class Spam(object):
    x=Descriptor()
s=Spam()
s.x=10
print(s.x)
print(Spam.__dict__)
class Integer:
    def __init__(self, name):
        self.storage_name = '_' + name  # 私有存储名
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.storage_name)
    
    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise ValueError(f"{self.storage_name} must be int")
        setattr(instance, self.storage_name, value)

class Point:
    __slots__ = ('_x', '_y')  # ✅ 槽名与描述器名分离
    x = Integer('x')          # 公开接口
    y = Integer('y')
    
    def __init__(self, x, y):
        self.x = x  # → Integer.__set__ → setattr(instance, '_x', x)
        self.y = y
# Descriptors in action
import stock
s=stock.Stock('GOOG',100,490.10)
print(s.name)
print(s.shares)
print(stock.Stock.__dict__.keys())
q=stock.Stock.__dict__['shares']
print(q.__get__(s))
q.__set__(s,75)
print(s.shares)
# Make your own descriptor
from descrip import Descriptor
class Foo:
    a=Descriptor('a')
    b=Descriptor('b')
    c=Descriptor('c')
f=Foo()
print(f)
f.a
f.b
f.a=23
del f.a
# From Validators to Descriptors
from validate import PositiveInteger
print(PositiveInteger.check(10))
s = stock.DeStock('GOOG', 100, 490.10)
print(s.shares)
s.shares=75
print(s.shares)
# 缓存
class CachedProperty:  
    def __init__(self, func):  
        self.func = func  
        self.__name__ = func.__name__  
         
    def __get__(self, instance, owner):  
        if instance is None:  
            return self
        print('Called get function')
        value = self.func(instance)  
        setattr(instance, self.__name__, value)  
        return value  
  
class MyClass:  
    def __init__(self, data):  
        self._data = data  
         
    @CachedProperty  
    def processed_data(self):  
        # Perform some slow computation  
        result = [x ** 2 for x in self._data]  # 补全：将每个元素平方
        return result
obj=MyClass([1,2,3,4,5])
print(obj.processed_data)
print(obj.processed_data)

# 只读控制
class ReadOnlyDescriptor:  
    def __init__(self, value):  
        self.value = value  
         
    def __get__(self, instance, owner):  
        return self.value  
     
    def __set__(self, instance, value):  
        raise AttributeError("can't set attribute")  
  
class MyClass:  
    def __init__(self, data):  
        self._data = ReadOnlyDescriptor(data) 

class NonDataDesc:
    def __get__(self, instance, owner):
        print('__get__ called')
        return 'from descriptor'
class B:
    attr = NonDataDesc()  # 非数据描述符（无 __set__）
b = B()
print(b.attr)
b.attr = 'instance value'  # ✅ 直接写入实例字典，不触发 __set__
print(b.attr)              # → 'instance value'（实例字典优先）
print(B.attr)              # → __get__ called → 'from descriptor' 

class DataDesc:
    def __get__(self, instance, owner):
        print(f'__get__: {instance=}, {owner=}')
        return instance.__dict__.get('attr', 'default')    
    def __set__(self, instance, value):
        print(f'__set__: {value=}')
        instance.__dict__['attr'] = value
class A:
    attr = DataDesc()  # 数据描述符（有 __set__）
a = A()
q=A.__dict__['attr']
print(q) # <__main__.DataDesc object at 0x00000279B19DA930>
q.__set__(a,43)
print(q.__get__(a,a.__class__))
class Descriptor:
    def __init__(self,name):
        self.name='_'+name
    def __get__(self,instance,cls):
        if instance==None:
            return self
        return getattr(instance,self.name)
    def __set__(self,instance,value):
        setattr(instance,self.name,value)
class A:
    __slots__=('_x','_y')
    x=Descriptor('x')
    y=Descriptor('y')
a=A()
a.x=10
a.y=20
print(a.x)
print(a.y)
class Mystatic:
    def __init__(self,func):
        self.func=func
    def __get__(self,instance,owner):
        # 无论是实例访问还是类访问都返回函数
        return self.func
class Math:
    @Mystatic
    def add(x,y):
        return x+y
print(Math.add(1,2))
m=Math()
print(m.add(2,3))
class Myclass:
    def __init__(self,func):
        self.func=func
    def __get__(self,instance,cls):
        def wrapper(*args,**kwargs):
            return self.func(cls,*args,**kwargs)
        return wrapper
class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
    
    @Myclass
    def today(cls):
        import datetime
        now = datetime.date.today()
        return cls(now.year, now.month, now.day)
d = Date.today()  # 通过类调用 → cls=Date
print(d.year)     # 2026（假设今天)
class Myproperty:
    def __init__(self,fget=None,fset=None,fdel=None,doc=None):
        self.fget=fget # gettr 函数
        self.fset=fset # settr 函数
        self.fdel=fdel # deleter 函数
        self.__doc__=doc or (fget.__doc__ if fget else None)
    def __get__(self,instance,owner):
        if instance is None:
            return self
        if self.fget is None:
            raise AttributeError("unreadable attribute")
        return self.fget(instance)  # 调用 getter
    def __set__(self,instance,value):
        if self.fset is None:
            raise AttributeError
        self.fset(instance,value)
    def __delete__(self,instance):
        if self.deleter is None:
            raise AttributeError
        self.fdel(instance)  # 调用 deleter
    def setter(self, fset):
        return type(self)(self.fget, fset, self.fdel, self.__doc__)
    def deleter(self, fdel):
        return type(self)(self.fget, self.fset, fdel, self.__doc__)
class Circle:
    def __init__(self, radius):
        self._radius = radius    
    @Myproperty
    def radius(self):
        """圆的半径"""
        return self._radius 
    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("半径不能为负")
        self._radius = value   
    @radius.deleter
    def radius(self):
        del self._radius
c = Circle(5)
print(c.radius)    # 5（触发 __get__ → fget）
c.radius = 10      # 触发 __set__ → fset
del c.radius       # 触发 __delete__ → fdel 