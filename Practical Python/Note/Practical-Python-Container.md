---
title: Practical-Python-Container
date: 2025-10-10 16:39:30
tags:
    - Computer Science
    - Python
categories: Python
mathjax: true
---

本笔记完全基于David Beazley的Python教程-[Practical Python](https://dabeaz-course.github.io/practical-python/Notes/Contents.html).

## 2.2 Container

Python中提供了存储多个对象的容器,主要为列表,字典或集合.列表一般用于存储有序数据;字典则是用于存储无需数据;集合则是与字典类似,但其用于存储无序且不允许重复元素的数据.

我们先介绍集合的概念,其的赋值方式和字典十分类似,但是不同的是他只存储元素值,而字典存储键值对.

```python
s={'IBM','GOOG'} # 集合赋值
d={'IBM':90.1,'GOOG':23.12} # 字典赋值
```

<!--more-->

字典和集合存储的都是无序数据,因此他们并不支持利用下标的方式索引,而是利用关键字的方式加以检索.但不同的是,由于字典和集合的赋值方式十分类似,因此我们需要指出二者的空集声明方式是不同的,如

```python
s=set() # 空集合
d={} # 空字典
s=set(['a','b','c','a'])
print(s) # {'a','b','c'}
```

从上面的赋值过程,我们发现其实我们是可以给集合赋值重复元素的,但是程序会自动清除重复元素,因此集合可用来处理程序中出现的重复元素.一般来说,字典的基本操作是键值之间的映射运算,而集合的基本操作则是集合运算,如

```python
s1={'a','b','c'}
s2={'c','d','e'}
s1|s2 # 集合并运算:a b c d e
s1&s2 # 集合交运算:c
s1-s2 # 集合差运算:a b
s1^s2 # 集合对称差运算:a b
s1.add('f') # 集合添加元素操作
s2.remove('a') # 集合删除元素操作
```

集合和字典一样,底层都是由Hash表实现,因此在字典和集合中查找元素所需的时间复杂度为O(1).

如果考虑的数据对数据顺序十分敏感,那么建议采用列表来存储数据.列表可以包含任何类型的数据对象.列表的构建可以从空列表开始,利用append方法不断延展列表内容.

```python
l=[]# 建立空列表
l.append(12)
l.append(12.34)
```

这里我们需要额外声明一下,如果我们想利用append方法往列表内输入元组,必须使用()来显式展示出我们输入的对象是元组,如果我们不加(),会让系统误认为输入了多个参数,从而导致程序报错.

如果考虑的数据需要快速随机查找或者频繁随机查找(随机查找就是按键查找),那么建议采用字典来存储数据.同样,字典的构造也是从空字典开始,而后不断追加字典元素.

```python
d={}
d['IBM']=90.2024
d['AA']=10.2
```

对字典的查找,我们可以利用in来完成查找,返回的值是True/False.这一般是用来判断字典中是否存在特定的键.但我们可能需要直接获取键对应的值,那么我们可以采用get方法,他有两个参数,第一个用于输入用于查找的键,第二个则是如果查找不到,则会输出的默认值.

```python
print('IBM' in d) # True
print('AA' not in d) # False
print(d.get('IBM',0.0)) # 90.2024
print(d.get('AB',0.0) # 0.0
```

字典的键并不是强制要求是字符串,但要求其是不可变的,如元组;列表,集合和其他的字典都不可以作为字典的键.

```python
holiday={
    (1,3):'New York',
    (5,6):'Wuhan'
}
print(holiday[1,3])
```


<a id="orgc8c4435"></a>

## 2.3 Sequence

Python中给出了三种不同的序列类型:字符串,列表和元组.序列指有序的数据结构,因此他们可以按整数下标进行索引,同时可以获取其长度.

```python
a='Hello' # String
b=[1,4,5] # List
c=('GOOG',100,490.1)

# Indexed order
print(a[0])
print(b[-1])
print(c[1])

# Length of sequence
print(len(a))
print(len(b))
print(len(c))
```

序列的基本操作:可以利用\*来重复序列数据;+用来串联两个相同类型的序列数据,一定要是相同类型的,不同类型会报错

```python
print(a*3)
print(b*2)
print(c*2)

a=(1,2,3)
b=(2,3,4)
print(a+b)
```

由于序列具有按下标索引的方式,因此序列可以做切片操作,从原序列中提取出子序列,其形式为s[start,end],其从s[start]一直提取到s[end-1].

```python
a=list(range(9))

print(a[2:5])
print(a[-5:])
print(a[:3])
```

序列切片的注意点:

1.  索引的开始和结束必须是整数
2.  切片提取的时候并不会提取尾值
3.  如果开始或结束有省略值,那么默认为序列开始或者末尾

序列的切片重赋值操作并不需要提取出的切片长度和赋值长度相同,程序会自己调整;可以利用del关键字,直接对序列的某段切片执行删除操作.

```python
b=list(a)
b[2:5]=[10,11,12,13,14]
print(b)
del b[2:5]
print(b)
```

序列的常用函数:sum(对序列元素求和),min(选取序列元素的最小值),max(选取序列元素的最大值).需要注意的是这里的sum并不能对字符串操作,min和max也不能让字符串和数字比较.

```python
t = ['Hello', 'World']
print(max(t))
print(max(max(t)))
```

序列迭代,其实是在迭代序列中的每个元素.每个循环会从序列中提取出一个值放入迭代量i中,再对迭代量i操作.每次循环都会对迭代量i进行覆盖,并且与C的for循环不同,Python的迭代量并不会因为循环结束而释放,并保留最后一次迭代值.

```python
s=[1,4,9,16]
for i in s:
    print(i)
    print(i)
```

类似C/C++,Python同样具有break和continue.break适用于跳出循环,但是他只能跳出一层循环,如果我们在嵌套循环中使用,那么break只能跳出当前最内层的循环.continue则是直接跳过本次循环进入下一次循环.

range函数可以创建一个可迭代对象,一般是用于for循环中.其语法形式为

```python
range(stop)
range(start,stop[,step])
```

start表示计数从start开始,如果不提供start,那么默认从0开始.stop表示计数到stop,但是不包括stop.step表示推进步长,默认是1.

```python
for i in range(10):
    print(i*i)
for j in range(10,20):
    print(j)
for k in range(10,51,2):
    print(k)
```

enumerate函数是用于将一个可遍历的数据对象组合为一个索引序列可以同时列出数据和数据下标,一般用于for循环中.他和直接用序列迭代的不同在于提供了额外的计数器来获得对应的数据下标.

```python
enumerate(sequence,[start=0])
```

sequence指序列或某种可迭代的对象,start表示下标计数开始的位置,默认是0.

```python
names=['Elwood','Jake','Curtis']
for i,name in enumerate(names):
    print('i=',i,'name=',name)
for i,name in enumerate(names,start=1):
    print('i=',i,'name=',name)
```

enumerate有个十分常见的应用场景,就是读取文件的行号.

```python
with open(file,'rt') as f:
  for lineno,line in enumerate(f,start=1):
    pass
```

对于元组列表,如果我们直接用一个迭代量进行迭代,那么他会赋值元组,并不是很好操作.我们可以用多个迭代量加以迭代,这样的好处是他会对元组进行解包,每个迭代量对应元组的相应量.这要求迭代量的数量必须与每个元组的项数匹配,列表中每个元组的项数必须相等.

```python
points = [
    (1, 4),(10, 40),(23, 14),(5, 6),(7, 8)
]
for x in points:
    print(x)

for x, y in points:
    print(x,y)
```

zip函数通过接受多个序列,将其组合之后创建一个迭代器,其类型为zip类型.如果接收到的多个序列长度不一样,那么zip函数的结果以最短的序列为基准.zip比较常见的应用其实是为了创建字典来构造键值对.

```python
columns = ['name', 'shares', 'price']
values = ['GOOG', 100, 490.1 ]
pairs = zip(columns, values)
d=dict(pairs)
```

<a id="orgaa2373f"></a>
