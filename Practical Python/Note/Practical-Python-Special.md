---
title: Practical Python-Special Methods and Exceptions
date: 2025-12-18 21:11:28
tags:
    - Python
categories: Practical Python
mathjax: true
---

本笔记完全基于David Beazley的Python教程-[Practical Python](https://dabeaz-course.github.io/practical-python/Notes/Contents.html).

## Special Methods

类可以定义特殊方法,这些方法对于Python是具有特殊含义的.他们一般在开头和结尾都会用\_\_,例如我们前面常用的\_\_init\_\_初始化函数.在此,我们只关注几个例子,作为范例.

<!--more-->

对象有两种字符串表示形式,一种是我们常用的str()函数,一种则是将要介绍的repr()函数

```python
from datetime import date
d=date(2025,12,18)
print(str(d)) # 2025-12-18
print(repr(d)) # datetime.date(2025,12,18)
```

str()函数我们前面已经介绍过了,在此我们只是提及一下其作用是输出一些适合展示的结果形式,他主要是在Python脚本的print中调用.repr()则是用于交互模式下的输出,他会生成更详细的表达形式.repr返回对象的官方字符串表示,其设计目标在于无歧义,尽量包含重建对象所需的信息,面向开发者/调试.在理想情况下,

```python
eval(repr(obj))==obj # True
```

这是一个约定,但并不是强制要求,repr是可以无法重建对象的,只需要保证对象描述的清晰即可.例如,如下的代码repr结果就是无法重建的,

```python
class A:
    pass
a = A()
print(repr(a))
# <__main__.A object at 0x0000019E611CD3D0>
```

上面提到了eval函数,eval函数的完整语法是

```python
eval(expression[,global[,local]])
```

这里eval执行的是表达式而不是语句,因此如果输入x=1,会报错,因为他是赋值语句.eval会将字符串做Python表达式来解析执行,并且返回表达式的值.eval中表达式的变量依赖于命名空间,其中的global和local以字典的形式提供,分别表示全局命名空间和局部命名空间.其先在局部命名空间搜索,再在全局命名空间搜索,如果二者都没有找到,就会抛出NameError异常.

```python
x=10
print(eval("x+1"))
print(eval("x+1",{"x":10}))
print(eval("a + b", {"b": 2}, {"a": 1}))
```

数学运算符实际上存在如下的方法调用

| 运算符   | 特殊函数              |
| -------- | --------------------- |
| a+b      | a.\_\_add\_\_(b)      |
| a-b      | a.\_\_sub\_\_(b)      |
| a\*b     | a.\_\_mul\_\_(b)      |
| a/b      | a.\_\_truediv\_\_(b)  |
| a//b     | a.\_\_floordiv\_\_(b) |
| a%b      | a.\_\_mod\_\_(b)      |
| a<<b     | a.\_\_lshift\_\_(b)   |
| a >> b   | a.\_\_rshift\_\_(b)   |
| a & b    | a.\_\_and\_\_(b)      |
| a ^ b    | a.\_\_xor\_\_(b)      |
| a \*\* b | a.\_\_pow\_\_(b)      |
| ~a       | a.\_\_invert\_\_()    |

容器的特殊方法:

| 运算符   | 特殊函数               |
| -------- | ---------------------- |
| len(x)   | x.\_\_len\_\_()        |
| x[a]     | x.\_\_getitem\_\_(a)   |
| x[a]=v   | x.\_\_setitem\_\_(a,v) |
| del x[a] | x.\_\_delitem\_\_(a)   |

其方法调用其实是分成两步:先是通过类.方法返回绑定方法,然后再调用这个绑定方法计算结果.我们用下面的代码将其拆分开

```python
s=Stock.cost # 绑定方法
s()# 方法调用
```

绑定方法其实就是调用类方法的时候忘记加上了尾随括号.因此绑定方法通常是粗心且不明显错误的常见来源或者某些难以调试的错误行为.

从上面的特殊函数中,我们其实可以知道存在一些如getattr,setattr等的函数,其中hasattr(item,iterable)是可以判断item是否在可迭代对象中. getattr的代码结构如下所示

```python
getattr(object, name[, default])
```

如果object中存在名为name的属性返回该属性的值;如果不存在且提供了default返回default;如果不存在且没有提供default,抛出AttributeError.


<a id="org0956886"></a>

## Defining new Exception

前面提到的异常其实也是通过类来定义的,一切的异常都是继承于Exception,

```python
class NetworkError(Exception):
    pass
```

异常一般是空类,用pass作为异常主体.因此我们可以基于此,创建用户自定义的异常层次结构

```python
class AuthenticationError(NetworkError):
    pass
class ProtocolError(NetworkError):
    pass
```

<a id="org7fad4ae"></a>
