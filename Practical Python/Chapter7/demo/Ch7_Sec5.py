class Foo(object):
    @staticmethod
    def bar(x):
        print("Foo.bar:", x)
Foo.bar(42)

class CLS:
    def bar(self):
        print(self)
    
    @classmethod
    def spam(cls):
        print(cls)
f=CLS()
f.bar()
CLS.spam()

import time
class Date:
    def __init__(self,year,month,day):
        self.year=year
        self.month=month
        self.day=day
    @classmethod
    def today(cls):
        t=time.localtime()
        return cls(t.tm_year,t.tm_mon,t.tm_mday)
d=Date.today()
print(d.year,d.month,d.day)
class NewDate(Date):
    pass
nd=NewDate.today()
print(nd.year,nd.month,nd.day)
class A:
    def normal_method(self):
        print("normal_method", self)
    @staticmethod
    def static_method(x):
        print("static_method", x)
a = A()

# 访问类属性
print(A.normal_method)       # <function A.normal_method at ...>
print(A.static_method)       # <function A.static_method at ...> ???  

# 访问实例属性
print(a.normal_method)       # <bound method A.normal_method of <__main__.A object ...>>
print(a.static_method)       # <function A.static_method at ...>

print(A.static_method is a.static_method)   # True

import weakref
class Solver:
    _instance=weakref.WeakSet()
    def __init__(self,name):
        self.name=name
        Solver._register(self)
    @staticmethod
    def _register(instance):
        Solver._instance.add(instance)
    @staticmethod
    def active_instances():
        return list(Solver._instance)
s1=Solver("A")
s2=Solver("B")
print([s.name for s in Solver.active_instances()])  # ['A', 'B']
del s1
import gc; gc.collect()  # 强制垃圾回收
print([s.name for s in Solver.active_instances()])  # ['B']

class DataStore:
    _open_files = {}
    def __init__(self, path):
        self.path = path
    def open(self):
        self.handle = DataStore._open_file(self.path)
    def close(self):
        DataStore._close_file(self.path)
    @staticmethod
    def _open_file(path):
        if path not in DataStore._open_files:
            DataStore._open_files[path] = open(path, "w")
        return DataStore._open_files[path]
    @staticmethod
    def _close_file(path):
        f = DataStore._open_files.pop(path, None)
        if f:
            f.close()

import threading
class Cache:
    _lock = threading.Lock()
    _data = {}
    def get(self, key):
        with Cache._acquire():
            return Cache._data.get(key)
    def set(self, key, value):
        with Cache._acquire():
            Cache._data[key] = value
    @staticmethod
    def _acquire():
        return Cache._lock
cache = Cache()
cache.set("a", 1)
print(cache.get("a"))  # 1
cache.set("b", 2)
print(cache.get("b"))  # 2
cache.set("a", 3)
print(cache.get("a"))  # 3

class Connection:
    _pool = []

    def __init__(self, id):
        self.id = id

    @staticmethod
    def create(id):
        if Connection._pool:
            obj = Connection._pool.pop()
            obj.id = id
            return obj
        return Connection(id)

    def release(self):
        Connection._pool.append(self)
c1 = Connection.create(1)
c2 = Connection.create(2)

c1.release()

c3 = Connection.create(3)
print(c3.id)  # 3
print(c1 is c3)  # True

class Point:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    @classmethod
    def from_tuple(cls,t):
        print(cls,t)
        return cls(t[0],t[1])
class SubPoint(Point):
    pass
a=Point.from_tuple((2,3))
b=SubPoint.from_tuple((2,3))