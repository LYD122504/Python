from datetime import date
import time
d=date(2012,12,21)
print(d)
print(repr(d))
class Date:
    def __init__(self,year,month,day):
        self.year=year
        self.month=month
        self.day=day
    def __str__(self):
        return '%d-%d-%d' % (self.year,self.month,self.day)
    def __repr__(self):
        return 'Date(%r,%r,%r)' % (self.year,self.month,self.day)
    @classmethod
    def today(cls):
        tm=time.localtime()
        self=cls.__new__(cls)
        self.year=tm.tm_year
        self.month=tm.tm_mon
        self.day=tm.tm_mday
        return self
d=Date(2012,12,21)
d = Date.__new__(Date)
d.__init__(2026, 2, 1)
print(d)
print(repr(d))
d=Date.today()
print(d)
print(repr(d))
# new instance
class Dog():
    def __new__(cls, *args, **kwargs):
        print("run the new of dog")
        #return super(Dog,cls).__new__(cls)
        return super().__new__(cls)  #两条return语句作用相同

    def __init__(self):
        print("run the init of dog")
        print(self)
        print(self.__class__)
a = Dog()
# new and init
class A(object):
    def __init__(self, *args, **kwargs):
        print("run the init of A")
    def __new__(cls, *args, **kwargs):
        print("run thr new of A")
        return object.__new__(B, *args, **kwargs)
class B(object):
    def __init__(self):
        print("run the init of B")
    def __new__(cls, *args, **kwargs):
        print("run the new of B")
        return object.__new__(cls)
a = A()
print(type(a))
b = B()
print(type(b))
# new and init parent
class Parent:
    def __init__(self):
        print("Parent.__init__ called")
    def __new__(cls, *args, **kwargs):
        print(f"Parent.__new__ called for {cls}")
        return super().__new__(cls)
class Child(Parent):
    def __init__(self):
        print("Child.__init__ called")
    def __new__(cls, *args, **kwargs):
        print("Child.__new__: returning Parent instance!")
        # 关键：返回父类的实例，而不是 cls（即 Child）
        return super().__new__(Child, *args, **kwargs)
c = Child()
print("type(c):", type(c))
# 单例模式
class Single:
    _instance=None
    @staticmethod
    def __new__(cls,name,age):
        if not cls._instance:
            cls._instance=super().__new__(cls)
        return cls._instance
    def __init__(self,name,age):
        self.name=name
        self.age=age
a=Single('James',42)
b=Single('Hinton',31)
print(id(a)==id(b))
class Singleton:
    __instance=None
    __first_init=False
    @staticmethod
    def __new__(cls,name,age):
        if not cls.__instance:
            cls.__instance=super().__new__(cls)
        return cls.__instance
    def __init__(self,name,age):
        if not self.__first_init:
            self.name=name
            self.age=age
            self.__first_init=True
a=Singleton('James',42)
b=Singleton('Hinton',31)
print(id(a)==id(b))
print(a.age,a.name)
print(b.age,b.name)
a.size = 19
print(b.size)

class PositiveInt(int):
    def __new__(cls,value):
        if value<0:
            value=0
        return super().__new__(cls,value)
x = PositiveInt(-5)
print(x)  # 0 （而非 -5）
class UpperStr(str):
    def __new__(cls, content):
        return super().__new__(cls, content.upper())
s = UpperStr("hello")
print(s)  # "HELLO"
# 工厂模式
class Shape:
    def __new__(cls,shape_type,*args):
        if shape_type=='circle':
            return super().__new__(Circle)
        elif shape_type=='square':
            return super().__new__(Square)
        return super().__new__(cls)
class Circle(Shape): pass
class Square(Shape): pass
obj = Shape("circle")
print(type(obj))
# 对象池
class LimitedInstances:
    _pool = []
    _max = 3

    def __new__(cls):
        if len(cls._pool) < cls._max:
            instance = super().__new__(cls)
            cls._pool.append(instance)
            return instance
        return cls._pool[len(cls._pool) % cls._max]
a=LimitedInstances()
b=LimitedInstances()
print(type(a))
# __del__ method
class Person(object):
    def __init__(self,name):
        self.name = name
    def __del__(self):
        print("实例对象:%s"%self.name,id(self))
        print("python解释器开始回收%s对象了" % self.name)
print("类对象",id(Person))
zhangsan  = Person("张三")
print("实例对象张三:",id(zhangsan))
print("------------")
lisi  = Person("李四")
print("实例对象李四:",id(lisi))
# 使用del删除引用时的调用情况
class Test:
    def __del__(self):
        print('删除引用')
t=Test()
c=t
del t
del c
print('-'*5)
# 创建多个实例对象并且删除
import time
class Animal(object):
    # 初始化方法: 创建完对象后会自动被调用
    def __init__(self, name):
        print('__init__方法被调用')
        self.__name = name
    # 析构方法: 当对象被删除时，会自动被调用
    def __del__(self):
        print("__del__方法被调用")
        print("%s对象马上被干掉了..."%self.__name)
# 创建对象
dog = Animal("哈皮狗")
# 删除对象
del dog
cat = Animal("波斯猫")
cat2 = cat
cat3 = cat
print("---马上 删除cat对象")
del cat
print("---马上 删除cat2对象")
del cat2
print("---马上 删除cat3对象")
del cat3
print("程序2秒钟后结束")
time.sleep(2)
# 对应引用个数
import sys
# sys.getrefcount用于测量引用对象的个数
class Test:
    pass
t=Test()
print(sys.getrefcount(t))
c=t
print(sys.getrefcount(t))
del c
print(sys.getrefcount(t))
del t
# weakref
class Foo:
    pass
import weakref
f=Foo()
fref=weakref.ref(f)
print(fref)
del f
print(fref())
import weakref
class Subject:
    def __init__(self):
        self._observers=[] # 存储弱存储
    def attach(self,observer):
        self._observers.append(weakref.ref(observer))
    def notify(self):
        # 清理已死亡的对象
        alive=[]
        for ref in self._observers:
            obs=ref()
            if obs is not None:
                obs.update()
                alive.append(ref)
        self.observers=alive
class Observer:
    def __init__(self,name):
        self.name=name
    def update(self):
        print(f"{self.name} received update")
subject = Subject()
obs1 = Observer("A")
obs2 = Observer("B")
subject.attach(obs1)
subject.attach(obs2)
subject.notify()  # A, B 收到通知
del obs1  # obs1 被回收
subject.notify()  # 仅 B 收到通知，obs1 自动清理
# Cach
class WeakCache:
    def __init__(self):
        # key → weakref to value
        # 当 value 无其他强引用时自动消失
        self._cache=weakref.WeakValueDictionary()
    def get(self,key):
        return self._cache.get(key)
    def set(self,key,value):
        self._cache[key]=value
class A:
    pass
cache=WeakCache()
obj=A()
cache.set("key1",obj)
print(cache.get("key1"))
del obj
print(cache.get("key1"))

class Manager:
    def __enter__(self):
        print('Entering')
        return self
    def __exit__(self,ty,val,tb):
        print('Leaving')
        if ty:
            print('An exception occurred')
m=Manager()
with m:
    print("Hello World!")

# Better output for representing objects
from datetime import date
d=date(2026,2,3)
print(d)
print(repr(d))
print(f'The date is {d!r}')
print('The date is %r' % d)
import stock
goog=stock.Stock('GOOG',100,490.10)
print(repr(goog))
a = stock.Stock('GOOG', 100, 490.1)
b = stock.Stock('GOOG', 100, 490.1)
print(a == b)
import reader
portfolio=reader.read_csv_as_instances('../Data/portfolio.csv',stock.Stock)
import tableformat
formatter = tableformat.create_formatter('text')
tableformat.print_table(portfolio, ['name','shares','price'], formatter)
import sys
class redirect_stdout:
    def __init__(self,outfile):
        self.out_file=outfile
    def __enter__(self):
        self.stdout=sys.stdout
        sys.stdout=self.out_file
        return self.out_file
    def __exit__(self, ty, val, tb):
        sys.stdout = self.stdout
with redirect_stdout(open('out.txt', 'w')) as file:
        tableformat.print_table(portfolio, ['name','shares','price'], formatter)
        file.close()