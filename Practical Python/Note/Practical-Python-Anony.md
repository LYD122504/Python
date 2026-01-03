---
title: Practical Python-Variable argument and Anonymous function
date: 2026-01-01 16:42:12
tags:
    - Python
categories: Practical Python
mathjax: true
---

本笔记完全基于David Beazley的Python教程-[Practical Python](https://dabeaz-course.github.io/practical-python/Notes/Contents.html).

## Variable argument functions

在我们前面介绍的函数模型中,函数的调用参数是固定的:

```python
def f(a,b,c):
    pass
```

这表示函数的参数数量固定,参数名称固定,外部调用必须要严格匹配.一旦程序需求变化,那么接口就会破坏兼容性.因此为了解决这一问题,Python引入可变参数,为了满足如下三个目标:接口数量稳定,调用方式自然以及函数内部能统一处理参数集合.

<!--more-->

位置可变参数\*args解决数量不确定的位置参数问题.

```python
def f(x,*args):
    print("x =", x)
    print("args =", args)
    print(type(args))
    f(1,2,3,4)
    f(1)
```

所有未被显式命名的位置参数会被按顺序收集为一个元组,这样的\*args是一种剩余参数捕获机制.这里我们要解释一下元组在这里的意义,因为参数在语义上是不可变输入,tuple强化了只读,结构化输入的概念,避免调用者误以为可以在函数内修改调用参数.这样的参数绑定发生在函数调用阶段,而不是函数体执行阶段.换言之,在进入函数体之前,解释器已经完成了参数数量校验,参数分流并构造出tuple.

由于位置可变参数只能表达顺序,但是实际上有很多参数本质上是行为开关,模式选择,可选策略等关键字参数.因此他们需要的是命名快+可选参数,故而python提供了关键字可变参数.

```python
def g(x,t,**kwargs):
    print("x =", x)
    print("t =", t)
    print("kwargs =", kwargs)
    print(type(kwargs))
    g(2,3,flag=True,mode='fast',header='debug')
    g(5,6)
```

所有没有被显式接收的关键字参数都被打包成一个字典.字典是因为关键字其实纯天然就有键值对.

可以将上面两个可变参数综合在同一个函数内

```python
def f(*args,**kwargs):
    print("args =", args)
    print("kwargs =", kwargs)
    f(1,2,3,flag=True,mode='fast')
    f()
```

这种一般出现在我们在写一个封装函数,我们并不关心具体参数,但是我们必须要把参数完整的转移给底层函数,如果我们不利用\*arg/\*\*kwargs,那么我们就要在外层函数中复制底层函数的参数列表,那么他的适用性就受到了极大限制.

```python
def wrapper(*args, **kwargs):
    preprocess()
    return target(*args, **kwargs)
```

上面的函数结构表示他接受任何合法调用形式,并且保证不丢失信息.这样一来,对于不同函数输入,他具有统一的结构,从而使得结果更具普适性.

我们经常使用的是元组和字典,但是函数需要的是单独变量,需要做一个解包.

```python
# Passing Tuples and Dicts
numbers=(1,2,3,4)
f(*numbers)
options={'flag':True,'mode':'fast'}
f(**options)
```

这样的数据结构在语义上等价与该函数的参数.数据结构可以直接映射为调用接口.元组args利用\*args扩展为变量参数;字典kwargs也可以利用\*\*kwargs扩展为关键字参数.


<a id="orga3c12d4"></a>

## Anonymous functions and lambda

匿名函数是没有名字的函数.在Python中,通过lambda关键字定义.其核心特征就是用一个表达式,临时定义一个函数.Python的基本语法:

```python
lambda parameter: expression
f=lambda x: x**2
f(3) # 9
```

这里需要注意的是lambda只能写一个表达式,表达式的值会自动返回,且不能写语句,只允许表达式.

lambda作为高阶函数的参数,这其实是lambda存在的根本理由.我们以列表的原地排序函数为例,对于字典列表而言,我们关键字参数函数来提供比较方式.

```python
def stock_name(s):
    return s['name']
portfolio.sort(key=stock_name)
pprint(portfolio)
```

这里的关键字参数key用来表示使用比较的关键字函数.由于上面的关键字参数函数,其实只是返回一个表达式的值,因此可以使用lambda函数将上面的逻辑更加清晰.

```python
portfolio.sort(key=lambda s:s['name'])
```

给几个额外的例子

```python
list(map(lambda x:x**2,[1,2,3,4]))
list(filter(lambda x:x>0,[-2,-1,0,1,2]))
data=[(1,3),(4,1),(2,2)]
sorted(data,key=lambda x:x[1])
```

lambda函数的作用还可以覆盖一些简短的一次性代码逻辑.这里的一次性代码逻辑指的是只涉及输入和输出的关系,不引入中间变量.

```python
sign=lambda x:-1 if x<0 else 1
sign(-3)
```

这里的if&#x2026;else&#x2026;是表达式,并不是语句,因此可以应用lambda函数.

lambda函数还可以作为回调函数或者临时行为的方式.这类的lambda的关键词是把行为当做参数传递.回调的思维常见的结构为

```python
def apply(f,x):
    return f(x)
```

这里的f并不是一组数据,而是是一个行为.换言之,f应该是一个函数,而lambda函数在这里的角色应该是临时定义角色,然后立刻使用.

```python
apply(lambda x:x+1,10)
apply(lambda x:x**2,10)
```

这里是因为回调行为并不需要关心函数的名字,只关心函数的行为.

lambda的限制在于lambda函数是需要被刻意设计的.lambda的不能做的场景如下:

1.  lambda不能写多行表达式
2.  lambda的表达式中不能出现变量赋值
3.  lambda函数中不能出现如for/while/try/with关键字
4.  lambda函数计算完表达式的值并且返回值,这里不能使用return关键字
5.  lambda函数中不能包含注释和文档字符串.

非法实例:

```python
lambda x:
    y=x+1 #y=x+1
    return y
```

这里的判断标准其实很简单,如果函数逻辑比较复杂,那么就不应该选择使用lambda.
