---
title: Practical Python-Producer/Consumer and Pipelines
date: 2025-12-28 17:39:10
tags:
    - Python
categories: Practical Python
mathjax: true
---

本笔记完全基于David Beazley的Python教程-[Practical Python](https://dabeaz-course.github.io/practical-python/Notes/Contents.html).

## Producer/Consumer Problems and Workflows

生成器generator是用来设置各种生产者/消费者问题和管道工具的解决方案.生产者-消费者问题是经典的并发问题之一,其基本思想是生产者负责产生数据;消费者则负责使用数据;两者之间通过某种缓冲区或者管道的方式进行数据交换.Python中的生成器则很适合实现这种模式,他们具有延迟求值的特性:生成器不会一次性返回所有数据,而是每次yield产生一个值给消费者.

<!--more-->

```python
#producer
def follow(f):
    '''生产者:从文件逐行读取数据'''
    while True:
        line=f.readline()
        if not line:
            break
        yield line # 生产数据
#consumer
with open('data.txt') as f:
    for line in follow(f): # 消费数据
        print(line.strip())
```

这里的follow(f)是生成器,每次for循环迭代的时候,他才读取文件的一行并且返回.for line in follow(f)是消费者,每次从生成器获取数据并进行处理.yield是连接生产者与消费者的桥梁,生成器每次暂停,等待消费者获取数据.这里我们可以看出生成器避免了一次性读取文件导致的大量内存占用的问题.

生成器的另一个重要的应用是数据处理流水线(pipeline).

```shell
producer->processing->processing->consumer
```

生产者用于生产原始数据;加工阶段对数据进行处理或过滤,可以有多个阶段;消费者使用处理后的数据.中间阶段既是消费者(消费前一阶段的数据),又是生产者(产生下一阶段的数据).

```python
# Producer
def producer():
    for i in range(10):
        yield i  # 生成 0~9 的整数
# Processing stage: square the number
def square(numbers):
    for n in numbers:
        yield n ** 2  # 消费并生成新的数据
# Processing stage: filter even numbers
def even_filter(numbers):
    for n in numbers:
        if n % 2 == 0:
            yield n  # 只输出偶数
# Consumer
def consumer(numbers):
    for n in numbers:
        print("Consumed:", n)
# 设置流水线
a = producer()
b = square(a)
c = even_filter(b)
consumer(c)
```

数据在各阶段之间以惰性迭代的方式传递,而不是一次性全部生成.

生成器的特点与优势:

1.  延迟计算: 数据在需要时才生成,适合大数据流或无限序列
2.  低内存占用: 不需要一次性存储所有数据,只保留当前迭代状态
3.  组合灵活: 可以轻松将多个生成器函数串联形成流水线;中间阶段可以修改,过滤或者扩展数据流
4.  简洁的生产者-消费者实现: 不需要额外的队列,锁等机制即可处理顺序数据流;如果需要多线程/多进程,可以在生成器基础上增加同步.

无限流处理:

```python
# 无限整数生成器
def naturals():
    n = 0
    while True:
        yield n
        n += 1
# 偶数过滤
def evens(nums):
    for n in nums:
        if n % 2 == 0:
            yield n
# 平方计算
def squares(nums):
    for n in nums:
        yield n ** 2
# Consumer：取前10个平方偶数
from itertools import islice
a = naturals()
b = evens(a)
c = squares(b)
for n in islice(c, 10):
    print(n)
```


<a id="orge7010f0"></a>

## Generator Expressions

生成器表达式可以认为是列表解析式的惰性版本,他们的形式上基本上完全一致只是用圆括号代替方括号,不立即生成结果,只在迭代时才计算.

```python
a=[1,2,3,4]
b=(2*x for x in a)
```

此时b不是列表,是一个Generator object,没有数据存储,只有生成规则.他与普通列表解析的区别为

| 方面             | 列表解析     | 生成器表达式      |
| ---------------- | ------------ | ----------------- |
| 是否立刻计算     | 是           | 否(惰性)          |
| 是否占用内存     | 保存完整列表 | 几乎不占用内存    |
| 是否可以重复使用 | 是           | 否(一次性)        |
| 主要用途         | 多次访问数据 | 流式计算,一次计算 |

因此这里需要提醒的是,生成器表达式只能使用一次,一旦消耗,不可以重复使用.

```python
nums=[1,2,3,4,5]
squares=(x*x for x in nums)
for x in squares:
    print(x)
for x in squares:
    print(x) # 什么都没有
```

这是因为生成器内部维护一个当前位置;迭代结束后,状态耗尽;不会自动重置状态.生成器表达式的通用语法结构为

```python
(expr for x in iterable if condition)
```

生成器还可以用于函数参数,

```python
sum(x*x for x in nums)
sum([x*x for x in nums])
```

这里的区别在于第二个做法会先生成一个完整列表,而第一鞥是边算边加.如果出现如下的条件,建议先使用生成器表达式作为函数参数:

1.  数据只遍历一次
2.  中间结果不需要保存
3.  函数本身是消费型(如sum,max,any,all)

生成器表达式适用于任意可迭代对象,

```python
a = [1, 2, 3, 4]
b = (x*x for x in a)
c = (-x for x in b)
for i in c:
    print(i)
```

他其实和前面的生产者/消费者问题一样.本质上是一样的,数据以"流"的形式经过一系列变换.

生成器的核心使用场景:

1.  用迭代而不是数据结构思考问题:生成器表示如何一步步处理数据,这对处理文件,日志分析,网络流,大规模数据十分重要.

2.  流式处理:经典例子,过滤文件的数据行

    ```python
    f = open('somefile.txt')
    lines = (line for line in f if not line.startswith('#'))
    for line in lines:
        ...
    f.close()
    ```

    文件不需要一次性读取入内存,每行只处理一次,非常适合大文件.

3.  内存效率和性能:生成器的优势不是"更快算法".而是更低峰值内存,更好的可组合性,更清晰的数据流结构.

itertools模块提供的是通用的迭代模式,零内存或极低内存开销,可以无限生成数据.本质上是把常见的for-loop模板封装成函数.

| 函数                  | 核心用途               | 基本用法示例        | 典型使用场景               | 重要注意事项              |
| --------------------- | ---------------------- | ------------------- | -------------------------- | ------------------------- |
| chain(a,b,&#x2026;)   | 顺序拼接多个可迭代对象 | chain(a, b)         | 多个数据源合并为一条数据流 | 不创建新列表,按顺序消费   |
| count(start=0,step=1) | 无限整数序列           | count(1)            | 生成索引,时间步,编号       | 无限生成,必须搭配终止条件 |
| cycle(s)              | 无限循环迭代           | cycle([1,2,3])      | 轮询资源,周期性模式        | 会缓存整个 s              |
| dropwhile(p,s)        | 丢弃开头满足条件的元素 | dropwhile(x<0,data) | 跳过文件头,前导无效数据    | 一旦失败,后续不再检查条件 |
| groupby(s,key)        | 按相邻键分组           | groupby(data,key=f) | 日志按字段聚类             | 数据必须先排序            |
| repeat(x,n)           | 重复常量值             | repeat(0,5)         | 填充,占位,参数广播         | n=None时为无限            |

对于一些功能单一的生成器函数其实可以直接写成生成器表达式.如原函数为

```python
def filter_symbols(rows, names):
    for row in rows:
        if row['name'] in names:
            yield row
```

生成器表达式为

```python
rows = (row for row in rows if row['name'] in names)
```

生成器表达式和 itertools对于管道搭建而言,是这个架构的"轻量级零件",用来消除不必要的中间函数,可以提升代码可读性和组合性.
