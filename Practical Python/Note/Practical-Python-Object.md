---
title: Practical-Python-Object
date: 2025-10-10 16:46:53
tags:
    - Computer Science
    - Python
categories: Python
mathjax: true
---

本笔记完全基于David Beazley的Python教程-[Practical Python](https://dabeaz-course.github.io/practical-python/Notes/Contents.html).

## 2.6 Objects

Python的赋值并非赋实际值,而是创建并赋值引用副本.

```python
a=[1,2,3]
b=a
c=[a,b]
```

这里我们设计了三个变量,但其实底层只有一个列表对象[1,2,3],有四个不同的引用指向他,如果我们修改其中任意一个量,都会导致所有引用的值变化.

```python
b.append(4)
print(a) # [1,2,3,4]
print(b) # [1,2,3,4]
print(c) # [[1,2,3,4],[1,2,3,4]]
```

因此对于任意一个引用副本的变化都会导致全局引用副本的数值变化.因此这与其他的语言十分不同,需要牢记修改的谨慎性.由于赋值并不是赋实际值,而是赋引用副本.那么对变量的重新赋值并不会修改先前指向的内存结果,而只是修改引用指向的位置.

is运算符可以用来判断两个变量是否对应相同的对象.其是通过比较对象身份的方式进行的,而对象身份则是用id()来获取.

```python
a=[1,2,3]
b=a
print(a is b) # true
c=[1,2,3]
print(a is c) # false
print(id(a)) # 2340643625152,每次运行都会不同
```

这里我们发现a和b是指向同一个对象,但是a和c却并不是,尽管a和c指向的对象值完全一样,这是因为尽管他们的指向的对象值一样,但是他们在计算机里面的逻辑存储位置不同,因此他们并不是同一个对象.但是我们可以利用==运算符来判断他们是否值相同,但值得注意的是变量具有相同的值并不一定代表指向相同的对象.

```python
print(a==b) # true
print(a==c) # true
```

对于列表和字典,除了赋值的方法获得副本,还可以通过复制的方式获得副本.需要指出赋值和复制的区别在于如果直接赋值,那么两个变量就会指向同一个对象,容易出现在程序其他地方修改导致的不可预测的错误;而复制只是复制对象的值,并不会指向相同的对象,可以保证独立性.

```python
# shallow copies
a=[2,3,[100,101],4]
b=list(a)
print(a is b) # false
print(a[1] is b[1]) # false
print(a[2] is b[2]) # true
```

这里我们发现如果我们用list()做浅复制,那列表内的基本数据类型项并不指向相同的对象,但拥有相同的值;而对于内部列表项(实际上,可以延拓到其他的序列类型),却是指向相同的对象,也就是修改任意一个变量的内部列表项是会传递到另一个,而如果修改其他的基本数据类型项则不会影响.

为了进一步完全的通过复制的方式获得全部数据项的副本,而不是某些项指向相同的对象,可以通过调用copy模块来完成这个操作

```python
# deep copy
import copy
a=[2,3,[100,101],4]
b=copy.deepcopy(a)
print(a is b) # false
print(a[1] is b[1]) # false
print(a[2] is b[2]) # false
```

deepcopy会将对象及其包含的所有对象一起复制,不会出现其中内嵌的序列类型项指向相同的对象.

类型检查:可以通过利用isinstance()函数来判断一个对象是否为特定类型.

```python
isinstance(variable,type)
if isinstance(a,list):
    print('a is a list')
```

我们可以利用元组的方式查找多个可能的类型:

```python
if isinstance(a,list):
    print('a is a list')
```

最好不要频繁使用类型检查.

