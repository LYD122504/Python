---
title: Practical-Python-Datatype
date: 2025-10-10 16:25:41
tags:
    - Computer Science
    - Python
categories: Python
mathjax: true
---

本笔记完全基于David Beazley的Python教程-[Practical Python](https://dabeaz-course.github.io/practical-python/Notes/Contents.html).

## 2.1 Datatypes and Data structures

None类型: None可选或缺失值的占位符.在条件语句中,认为是False.

元组指的是一组值的组合,其利用如下的方式声明,

```python
s=('GOOG',100,49.1)
s='GOOG',100,49.1
```

<!--more-->

()的存在对于定义元组并不是重要的,可以舍去.而我们还有如下两种特殊情况,

```python
s=() # 0元组
s=('GooG',) # 一元组
s='GOOG', 
```

这里需要注意的是一元组的声明是必须要有,在末尾的,否则会被视作基本数据类型.零元组的定义声明则必须要存在(),否则将无法区分语法错误和赋值.

元组通常用于表示简单的记录或者结构.他是一个由多部分组成的单个对象,其包含的多个部分是允许具有不同的数据类型的.和列表一样,他也是一个有序集合,也就是他可以通过下标索引得到对应的值.但不同在于他无法修改元组内容,虽然我们可以通过当前元组去生成一个新元组的方式来覆盖原元组,但其与修改还是有执行逻辑上的差异.

```python
s=(s[0],75,s[2])
```

我们可以认为元组是把几个相关对象打包成一个实体对象,这样的话,可以在函数调用之中同时传输几个相关对象.元组解包的方式则是利用左侧变量的赋值来获得,但要求左侧变量的数量与元组结构内的相匹配,至于类型则并不需要,因为Python的变量类型是可以通过程序自动调整的.

```python
names,shares,prices=s
```

从我们上面的讨论中,元组可以被认为是只读列表,但一般而言,列表存放多个独立变量对象的数据集合,而元组则是描述一个不会改变的事物的属性.

字典则是对于键与值的映射,所以其是键对的集合,这个与Hash表,关联数组十分类似,都可以通过键来访问对应的值.如

```python
d={
    'name': 'GOOG',
    'share':100,
    'prices':470.10
}
print(d['name'])
```

与元组不可修改的性质不同,字典可以根据键名赋值的方式来修改或添加字典值,

```python
s['shares']+=100
print(s['shares'])
s['date']='6/6/2024'
print(s)
```

如果希望删除字典中的某个键对,我们可以利用del关键字来完成删除操作.

```python
del s['date']
print(s)
```

对于字典,有如下额外的操作

```python
l=list(d) # 利用list()函数可以将字典的所有键提取成一个列表
print(l)
```

list函数会默认读取字典的键,换言之,字典其实有点像是某种意义的封装实体,外界访问字典仅可以通过其键来访问他的值,故而其读取会默认读取字典的键.所以从这个角度来看,如果利用for循环迭代访问字典,迭代的结果其实就是字典的key.

字典提供了一个keys()方法来提取字典的键,其结果并不是常见的数据类型,而是dict\_keys,他是一个关于字典键的动态视图.

```python
keys=d.keys()
print(keys)
del d['account']
print(keys)
```

这个动态视图的动态性指的是他可以同步更新对相关字典的改变,而不需要通过再赋值的方式来修改.同样,字典还提供了提取字典值的方法values,其结果类型是dict\_values,他是关于字典值的动态视图.还提供了提取字典键值对的方法items,其结果类型是dict\_items,他则是关于字典键值对的动态视图. 如果我们存在一个已知的dict\_items类型,可以利用dict函数直接生成一个字典.

```python
d_item=d.items()
print(d_item)
dnew=dict(d_item)
print(dnew)
```

值得注意的是,这些东西只是提供了字典的某种动态视图,他并不支持下标访问也不支持修改,如果需要修改,那么需要修改原字典.

<a id="org3dadcbf"></a>
