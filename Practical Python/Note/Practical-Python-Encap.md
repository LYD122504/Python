---
title: Practical Python-Encapsulation
date: 2025-12-22 11:29:16
tags:
    - Python
categories: Practical Python
mathjax: true
---

本笔记完全基于David Beazley的Python教程-[Practical Python](https://dabeaz-course.github.io/practical-python/Notes/Contents.html).

## Encapsulation Techniques

类的使用会试图封装内部实现细节.因为类的主要作用之一是封装对象数据和内部实现细节,但是会提供一些public接口供外部调用.这一特点在C++体现的尤为明显,他通过严格的访问控制机制来实现代码的封装.但是Python中并没有提供严格的封装机制以及访问控制机制.

<!--more-->

1.  Python可以轻松地检查对象内部结构
2.  Python可以任意修改对象内部数据
3.  Python并没有严格的访问控制概念

Python基于变量命名形成某种约定俗成的规定,\_name认为他是私有变量,虽然我们还是可以直接访问并修改这些数据.但是一般来说我们认为当我们开始在外部操作\_name变量的时候,程序可能已经发生了错误,\_name默认为类的内部实现,通过程序员的约定俗成维护.

```python
class Person(object):
    def __init__(self,name):
        self._name=name
p=Person('Guido')
print(p._name)
p._name='Dave'
print(p._name)
```

在类中其实有一个比较大的问题,因为Python是一个动态语言,因此我们可以将属性修改为任意类型的值,但不会报错.然而,类型的变化可能影响我们后续代码的运行,因此我们需要控制这个风险.

```python
class Stock:
    def __init__(self, name, shares, price):
        self.name = name
        self.shares=shares
        self.price = price
s=Stock('IBM',50,91.1)
print(s.shares)
s.shares="hundred"
print(s.shares)
s.shares=[1,0,0]
print(s.shares)
```

第一种方式其实十分简单,就是在赋值之前我们做一个类型检测,并且将变量做成内部变量.

```python
class Stock:
    def __init__(self, name, shares, price):
        self.name = name
        self.set_shares(shares)
        self.price = price
    def get_shares(self):
        return self._shares
    def set_shares(self,value):
        if not isinstance(value,int):
            raise TypeError("Expected an int")
        self._shares=value
```

但是他有一个问题,就是原代码中我们提取shares属性都是通过.shares来实现的,他则需要将其改成使用.get\_shares()的方法来实现.如果代码量较大的时候,修改将会十分复杂.因此我们给出另一种方法来对他做实现.

在给出方法之前,我们先介绍Python中一个十分重要的机制:装饰器机制.装饰器本质上其实就是Python中的一个函数或者类,他可以在不改动原有代码的基础上使得现有函数增加某些额外功能.以函数装饰器为例,他可以应用在日志插入,性能测试等具有切面需求的场景.切面指的是如函数的进入和退出,称之为一个横切面,这类编程方式则是面向切面的编程.

我们先给出不使用装饰器的结果

```python
import logging # 导入日志模块
logging.basicConfig(level=logging.INFO)# 把info放行,因为正常的是warning
def f():
    print('Here is function f')
    logging.info('function f is running')
```

但这样的话,我们在大量函数中会出现雷同的logging.info函数,因此我们可以选择写一个函数专门完成这样的重复工作,即

```python
def log(func):
    logging.info('function %s is running' % func.__name__)
    func()
def f():
    print('Here is function f')
log(f)
```

这样虽然可以避免写大量重复的logging.info函数,但是他将函数调用修改成了log(f),修改量又太多了.因此,我们其实很自然可以想到将一个函数传入之后,返回的时候也是一个函数,这其实就是装饰器的思想,通过对现有函数的包装,实现功能的添加组合.

```python
def log(func):
    def deco(*args,**kwargs):
        logging.info('function %s is running' % func.__name__)
        return func(*args,**kwargs)
    return deco
def f():
    print('Here is function f')
f=log(f)
f()
```

这里的log其实就是一个装饰器,他将真正的函数f包裹在了函数deco中并且返回了deco.所以实际上虽然我们用的是f=log(f),这个赋值后的f他的\_\_name\_\_应该是deco.换言之,f其实就是函数deco,他会丢失原有的名字和文档,后面我们将给出一个方法来保留原有的内容.Python为了避免二次赋值,提供了@符号,其为装饰器的语法糖,他在定义函数时直接使用

```python
def log(func):
    def deco(*args,**kwargs):
        logging.info('function %s is running' % func.__name__)
        return func(*args,**kwargs)
    return deco
@log
def f():
    print('Here is function f')
f()
```

装饰器在Python使用极其便利,是因为Python的高度自由,如Python中的函数可以像普通参数一样传入,赋值和返回,并且允许函数的嵌套定义.

在上面的装饰器的基础上,我们还可以对装饰器再做一次封装,这次封装,可以给装饰器加上参数以扩展能力.

```python
def log(level):
    def deco(func):
        def wrap(*args,**kwargs):# 保证被装饰函数 func 可以是任意参数形式
            if level=='info':
                logging.info('function %s is running' % func.__name__)
        return func(*args,**kwargs)
        return wrap
    return deco
@log('info')
def f():
    print('Here is function f')
f()
```

除了函数装饰器,我们还可以写一个类装饰器,其具有灵活度大,高内聚,封装性等优点.同时如果利用类装饰器封装函数,我们还可以用\_\_call\_\_内部调用函数来使用,自动调用函数.

```python
class F(object):
    def __init__(self,func):
        self._func=func
    def __call__(self):
        print('class decorator running')
        self._func()
        print('class decorator ending')
@Foo
def bar():
    print('bar')
bar()
print(type(bar))
```

这里的bar已经不再是函数,而是类对象.

上面我们提到过通过装饰器包装后的函数会丢失函数的原名和注释.Python为此提供了functools.wraps,wraps其实也是一个装饰器,他可以将原函数的元信息复制到装饰器函数中,从而避免赋值后丢失信息的问题,但其实本质上还是另一个函数.

```python
def logged(func):
    @wraps(func)
    def with_logging(*args,**kwargs):
        print(func.__name__+' was called')
        return func(*args,**kwargs)
    return with_logging
@logged
def f(x):
    '''does some math'''
    return x+x*x
print(f.__name__)
print(f.__doc__)
```

装饰器是允许叠用的,如

```python
@a
@b
@c
def f:
    pass
f()
```

他相当于f=a(b(c(f))).Python中也提供了几种较为常用的装饰器,@staticmethod,@classmethod和@property.我们提到的第二种方法将会基于@property装饰器展开.

我们先给出第二种方法的代码实现

```python
class Stock:
    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

    @property
    def shares(self):
        return self._shares

    @shares.setter
    def shares(self, value):
        if not isinstance(value, int):
            raise TypeError('Expected int')
        self._shares = value
```

这个代码的作用是将shares属性设置成了一个受控属性,在不改变属性访问语法的情况下,多了对赋值进行类型校验的过程.他对外表示的形式是通过shares属性,对内则是用\_shares完成私有化.第一个property表示定义一个名为shares的property并且shares(self)的方法作为这个属性的取出方法,对外的表现其实仍然是一个属性.第二个@shares.setter,则是给已存在的property对象添加写入逻辑,他不会拓展新的属性,而是增强原有property的能力.这里我们需要注意的是他内部用\_shares实现存储,其实不仅仅是为了封装,而是为了防止在setter装饰器中出现死循环.如果仍然使用shares,那他会在self.shares=value里不断循环并无法跳出.我们可以用如下方式验证shares其实不是一个属性

```python
print(Stock.__dict__['shares'])
```

同样property装饰器也可以作用到方法上,这样可以允许我们省略括号,使得方法和属性在形式上一致.

```python
class Stock:
    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

    @property
    def cost(self):
        return self.shares * self.price
s=Stock('GOOG', 100, 490.1)
print(s.shares)
print(s.cost)
```

<a id="org57cd970"></a>
