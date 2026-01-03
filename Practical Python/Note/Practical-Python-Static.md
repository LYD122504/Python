---
title: Practical-Python-Static
date: 2026-01-03 16:50:47
tags:
    - Python
categories: Practical Python
mathjax: true
---

<a id="org1dfe10a"></a>

本笔记完全基于David Beazley的Python教程-[Practical Python](https://dabeaz-course.github.io/practical-python/Notes/Contents.html).

## Static and class methods

我们之前介绍了装饰器和一些Python预定义的装饰器.这些预定义装饰器是用于在类中定义中指定特殊类型的方法.一般有staticmethod,classmethod和property.其中property,我们前面已经介绍过了property,他将类中的方法伪装成属性.通过property,可以在保持对象接口简洁的同时,对属性访问进行控制.

<!--more-->

Python中,静态方法是定义在类内部,但是不依赖实例状态或类状态的方法.与普通示例方法不同,静态方法在调用的时候不会自动接受实例状态参数self;与类方法不同,他也不会接收类状态参数cls.从实现机制来看,@staticmethod的作用是阻止函数在类属性访问时发生方法绑定,因此无论通过类还是实例访问,得到的都会是同一个普通函数对象.

```python
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
```

我们可以从输出中发现,类的实例化并不会将函数绑定.实际上,staticmethod可以认为就只是普通函数,只不过他在类内部定义,体现一种逻辑归属.

在工程上,静态方法经常用于实现类的内部支撑性代码,其特点是服务于类的整体行为,常以工具性或基础设施存在,不应暴露为实例的公共接口,他们往往负责实例创建,资源管理或内部协作机制.在此我们给出一些简短的示例代码以解释其应用.

```python
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
import gc
gc.collect()  # 强制垃圾回收
print([s.name for s in Solver.active_instances()])  # ['B']
```

这里我们简要介绍一下Python的weakref机制.weakref是用于创建对象的弱引用的模块,其核心特征是不增加对象的引用计数,因此不会阻止垃圾回收.

1.  强引用: 普通变量名,容器中的对象
2.  弱引用: 只用于观察对象是否存在,不延长对象的生命周期

如缓存注册表,对象生命周期跟踪等场景,我们希望的是检测对象,但不希望影响对象的生命周期,所以需要用weakref.常用代码例子

```python
import weakref
class A:
    pass
a = A()
r = weakref.ref(a)
r()        # 返回 a
del a
r()        # 返回 None
```

```python
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
```

这个类的设计意图是多个实例共享同一个底层文件对象,避免出现重复open(path),集中管理文件的打开与关闭,这是一个较为典型的类级资源池.如果类考虑的文件是全局唯一资源,明确规定谁关闭,谁负责所有使用者,例如单例文件/日志文件,但如果多实例并发使用或生命周期独立的文件读取就不适用.静态方法在此的作用是管理全局类资源,实例只请求资源,但不涉及管理,并且不会污染实例接口.

```python
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
```

threading是一种用于多线程并发编程的模块,提供了在同一进程内并发执行多个控制流的能力.线程可以简单的认为是程序中的一条执行路线,一个进程里可以有多个线程,共享同一块内存空间,并同时推进代码执行.在多线程环境中,多个线程会同时访问共享数据.Lock则是一种互斥锁,是一种保证同一时间只有一个线程进入临界区的同步工具.他的基本行为:

```python
lock=threading.Lock()
lock.acquire() # 请求锁
lock.release() # 释放锁
with lock:
    pass
# 进入with获得锁,退出with释放锁
```

这里可能会出现死锁的地方在于threading.Lock不可重入,也就是同一个线程不能重复获得同一把锁.也就是如果代码形式如下:

```python
with Cache._acquire():
    r=Cache._acquire()
    Cache._data[key] = value
```

这样就会发生死锁现象.与Lock相反的是,RLock允许同一线程多次进入临界区,这样的话就不会发生上述的死锁现象.

```python
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
```

这个类的目标是维护一个可复用的对象池,优先从池中取已有对象,用完后把对象放回池中,降低创建对象的成本.用回收再利用代替反复new/delete.例如如下的代码

```python
c1 = Connection.create(1)
c2 = Connection.create(2)
c1.release()
c3 = Connection.create(3)
c3 is c1   # True
```

这里的c3就是复用了c1对象的结果.他适合用于创建成本高的对象,可重复使用的资源,链接,缓冲区和临时计算对象.但是上面只是一个简单的demo,并不涉及对象的状态重置.

类方法是一种绑定到类对象本身的方法,而不是绑定到实例.他的第一个参数约定为cls,表示当前类.

```python
class A:
    @classmethod
    def func(cls,x):
        print(cls,x)
A.func(x)
a=A()
a.func(x)
```

两种方法都可以,返回的类名称都是A.静态方法的本质是阻止实例化的时候方法被绑定,而类方法则是强制绑定到类对象.

类方法可以用于设计一些操作或查询类级状态的函数

```python
class Counter:
    count=0
    def __init__(self):
        Counter.count+=1
    @classmethod
    def how_many(cls):
        return cls.count
```

这里的count是类属性,因此访问他的函数how\_many应该自然的属于类的行为,而不归属于特定的实例,故而利用classmethod将其绑定到类上.

由于他是绑定在类上的,所以他在继承上具有较为优秀的表现,从下面的代码,

```python
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
a=Point.from_tuple(2,3)
b=SubPoint.from_tuple(2,3)
```

此时a返回的类名是Point,而b的返回类名是SubPoint,这是因为b的类是SubPoint,他是继承父类的方法,但还是靠SubPoint去调用的.而且这样并不会硬编码类名,硬编码类名会导致程序灵活性不够.
