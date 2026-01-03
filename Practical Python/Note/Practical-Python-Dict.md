---
title: Practical Python-Objects and Dictionaries
date: 2025-12-21 20:15:24
tags:
    - Python
categories: Practical Python
mathjax: true
---

本笔记完全基于David Beazley的Python教程-[Practical Python](https://dabeaz-course.github.io/practical-python/Notes/Contents.html).

## Dictionaries Revisited (Object Implementation)

Python的对象在系统底层很大依赖于字典构建.换言之,Python对象本质上存放在一个字典里.

在模块内部,字典会存放模块中所有的全局变量和函数.

<!--more-->

```python
# foo.py
x=42
def bar():
    pass
def spam():
    pass
print(globals())
# main.py
import foo
print(foo.__dict__)
```

我们前面提到的类的数据实际上也是存放在字典里的,定义的类其实可以看成对底层的一个封装.实例属性是存放在实例的\_\_dict\_\_字典中,他存放的是通过\_\_init\_\_函数初始化的实例属性或者代码运行中动态维护的实例名.变量名的方式.

```python
class A:
    x = 1
    def __init__(self,num):
        self.num=num
                a = A(10)
                a.x = 100     # 实例属性，遮蔽类属性
                print(a.__dict__)   # 'x':100 'num':10
```

这里我们会发现实例属性里面没有初始化函数\_\_init\_\_,这是因为初始化函数其实是类的方法,实例是类的实例化,因此可以调用其,但其自身是没有函数的.所以从这里我们就可以知道Python为什么可以在程序运行中动态增加实例属性了,因为他的实例属性的存储实际上就是维护实例字典的过程,动态增加实例属性,只不过是修改实例字典的过程.并且每个实例都会具有自己独特的实例字典,有多少个实例就会存储多少个实例字典.

类属性和类方法都会存储在类字典里.

```python
class A:
    x=1
    def func(self):
        return A.x
    print(A.__dict__)
```

其结果比较多,我们稍微对每个结果加以解释.\_\_module\_\_映射的是类定义在的模块名,如果直接运行得到的就是\_\_main\_\_;类属性的对应关系,函数会返回一个<function>对象,后续我们会提到,不再赘述;\_\_dict\_\_他的返回不是一个字典,而是一个<attribute>对象,我们会在下面详细解释,他的作用是定义A的实例如何拥有并访问实例字典;\_\_weakref\_\_则表示一个弱引用机制.

描述器(Descriptor)是Python对象模型里的一个协议,他可以控制属性访问行为,换言之,他其实就是类属性级别的访问控制器,决定你访问属性时发生什么.如果一个对象实现了以下三个方法的任意一个就可以认为其是描述器:

```python
__get__(self,instance,owner)
__set__(self,instance,value)
__delete__(self,instance)
```

如果只实现了\_\_get\_\_,那么他是non-data descriptor;如果实现了\_\_set\_\_或\_\_delete\_\_,那么他是data descriptor.non-data descriptor可以被实例属性覆盖,data descriptor不允许实例属性覆盖.

非数据描述器的例子比较常见的就是类中的函数:

```python
class A:
    def f(self):
        return "method called"
    a=A()
    # a.f调用function的 __get__,返回bound method
print(a.f())   # "method called"
# 实例属性遮蔽non-datadescriptor
a.f = "instance attribute"
print(a.f)     # "instance attribute"(覆盖了 class的f)
```

上述的例子我们可以看出他会被实例属性覆盖.

数据描述器的例子:property实现了\_\_get\_\_和\_\_set\_\_,我们会在下一节内容进一步说明.

```python
class B:
    def __init__(self):
        self._x=10
        @property
    def x(self):
        return self._x
    b=B()
    print(b.x) # 10

b.__dict__['x'] = 999
print(b.x)  # 10(data descriptor优先,实例字典被遮蔽)
```

我们虽然在b中添加了实例属性x,但是Python会先查找类字典的data descriptor,关于其的访问永远优先于实例字典.

我们在此解释一下上面提到的两个对象为什么会是解释器.我们从函数出发,其代码如下,

```python
class A:
    def f(self):
        return 1
    a=A()
    print(A.__dict__['f']) # function 对象
    print(A.__dict__['f'].__get__(a,A) # bound method
```

这里的A.\_\_dict\_\_['f']是一个function对象,function对象在底层实现了一个\_\_get\_\_方法,他返回的会是一个绑定对象,因此前面说的a.f其实和如下代码一样

```python
A.__dict__['f'].__get__(a,A) # 绑定方法
```

这个function对象其实是一个非数据描述器,他不会覆盖实例属性.

特殊属性\_\_dict\_\_是描述器,他的作用是用来访问实例字典.

```python
class A:
    pass
a=A()
print(A.__dict__['__dict__']) # attribute对象
```

这个attribute属性在底层实现了\_\_get\_\_函数,不允许随便\_\_set\_\_或\_\_delete\_\_.我们访问a.\_\_dict\_\_时,底层实现如下

```python
print(A.__dict__['__dict__'].__get__(a,A))
```

他会返回一个实例字典,这个优先级高于实例字典,他可以控制字典的访问.他提供了安全访问实例字典的方法,可以防止破坏对象内部结构,是对象模型里最基础的描述器之一.

综上,我们可以给出基于字典的查找属性方法的代码.为了判断描述器具体为数据描述器还是非数据描述器,我们先给出如下的判断函数

```python
def is_data_descriptor(attr):
    return hasattr(attr,"__set__") or hasattr(attr,"__delete__")
def is_non_data_descriptor(attr):
    return hasattr(attr,"__get__")
```

这里的hasattr函数表示如果对象有该属性则返回true否则返回false.加入描述器判断的getattr函数实现如下

```python
def getattr(obj,name):
    cls=obj.__class__
    # 查找MRO顺序的数据描述器
    for base in cls.__mro__:
        if name in base.__dict__:
            attr=base.__dict__[name]
            if is_data_descriptor(attr):
                return attr.__get__(obj,cls)
            # 查实例字典
    if name in obj.__dict__:
        return obj.__dict__[name]
    # 查非数据描述器或者普通类属性
    for base in cls.__mro__:
        if name in base.__dict__:
            attr = base.__dict__[name]
            if hasattr(attr, "__get__"):
                return attr.__get__(obj, cls)
            return attr
    raise AttributeError(name)
```

可以用一些简单的例子加以测试,不再赘述.

最后,我们介绍一下\_\_slots\_\_属性,在前面中我们提到了对象的属性在底层是利用字典维护的,并且这个字典可以动态增加,并且每个实例都有自己的实例字典,但这样的维护在大量实例的情况下十分消耗计算资源.\_\_slots\_\_属性则是提供了一种静态属性表,实例并不会创建实例字典,而是只能存放制定字段的结果.

```python
class A:
    __slots__ = ('x',)
print(A.__dict__)
print('__dict__' in A.__dict__)   # False
print('x' in A.__dict__)          # True
a=A()
print(a.__slots__)
```

这样的A.\_\_dict\_\_返回中不会有\_\_dict\_\_,因为他的实例并不会创建实例字典,其通过\_\_slots\_\_维护一个静态属性表.

<a id="orge2379c0"></a>
