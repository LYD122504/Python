---
title: Practical-Python-Collection
date: 2025-10-10 16:42:53
tags:
    - Computer Science
    - Python
categories: Python
mathjax: true
---

本笔记完全基于David Beazley的Python教程-[Practical Python](https://dabeaz-course.github.io/practical-python/Notes/Contents.html).

## 2.4 Collection module

collection模块提供了一些用于数据处理的对象.如Counter计数器,defaultdict和deque等.在此我们只介绍这三个对象.

Counter其实是字典的一个子类,他与普通的字典的区别在于,他的键为待计数的元素,他的值为计数值或其余相关的数据;因此他的值虽然是计数值,但实际上是允许出现0或者负值的.此外,如果我们在字典中查找一个不存在的键,那么会返回一个KeyError异常,而如果对于Counter类查找一个不存在的键,他并不会报错,并且返回0,同时创建一个新键值对,计数值设为0.

<!--more-->

Counter常见的实例化方法如下:

```python
from collections import Counter
d=Counter() # 实例化一个空对象
d=Counter(iterable objective) # 实例化一个可迭代对象,其元素为可迭代对象的元素,并且对应的count值设定为1
d=Counter(mapping objective) # 实例化一个映射对象,这里的赋值会依赖于映射的值,此处可以将count值赋为其他类型的值
d=Counter(a=1,b=2,c=3) # 利用关键字参数实例化
```

这里虽然Counter类是字典类的一个子类,所以他其实并没有顺序,但print的顺序是依据键值的大小顺序排列,从大到小排序.还有一个地方需要注意的是如果以字典来实例化Counter类,字典的键可以重复,如果出现了多次相同的键,那么他会保存最后一个键值对,因此利用字典实例化Counter类的话,是可以出现重复的键.但是如果选用利用关键字参数实例化,那么并不可以这样,如果出现了多个相同的关键字,那么他就会报SyntaxError异常.

Counter的常用方法是most\_common(n).他的作用是输出计数值最大的n个对象.如果n小于Counter类的元素总数,那么输出的结果就是n个Counter类计数值最大的前n个元素;如果n大于等于Counter类的元素个数,那么相当于直接输出Counter类的所有元素;如果没有输入n,那么也是默认输出全部元素;如果输入n=-1,那么返回空列表.这里我们需要强调一点的是Counter的most\_common(n)返回的并不是Counter类,而是列表类型.

```python
print(d.most_common(3))
```

普通的字典是一对一的映射,也就是一个键只能对应一个值;我们可以利用的defaultdict来完成一对多的映射,其基本语法为

```python
from collections import defaultdict
d=defaultdict(default_factory)
```

这里的default\_factory是一个可调用对象(比如int,list,set,str),用于生成默认值.如果在defaultdict中查找一个不存在的键,他并不会报错,而是依据可调用对象的方式生成一个默认值.例如int对应的默认值为0,list对应的默认值为[],set对应的默认值为set(),str对应的默认值为''.因此他的一对多映射由如下形式定义:

```python
from collections import defaultdict
d=default(list)
d=['x'].append(10)
d=['x'].append(20)
print(d)
```

deque是双端队列,因此他的队列两端的插入删除操作时间复杂度为O(1).当然可以把他当做stack或者queue使用,只需要调用输入输出方法的时候控制两端的输入输出.其基本语法为:

```python
from collections import deque
d=deque(iterable=None,maxlen=None)
```

其中的iterable表示可以输入一个可迭代对象,用来初始化队列;maxlen表示双端队列的最大长度,如果超过了这个长度,那么就从另一端弹出元素.队列常用的操作如下

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">



<colgroup>
<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">方法</th>
<th scope="col" class="org-left">功能</th>
<th scope="col" class="org-left">示例</th>
</tr>
</thead>

<tbody>
<tr>
<td class="org-left">append(x)</td>
<td class="org-left">在右端添加元素</td>
<td class="org-left">d.append(i)</td>
</tr>


<tr>
<td class="org-left">appendleft(x)</td>
<td class="org-left">在左端添加元素</td>
<td class="org-left">d.appendleft(i)</td>
</tr>


<tr>
<td class="org-left">pop()</td>
<td class="org-left">弹出右端元素</td>
<td class="org-left">d.pop()</td>
</tr>


<tr>
<td class="org-left">popleft()</td>
<td class="org-left">弹出左端元素</td>
<td class="org-left">d.popleft()</td>
</tr>


<tr>
<td class="org-left">extend(iterable)</td>
<td class="org-left">在右端批量添加元素</td>
<td class="org-left">d.extend([3,4])</td>
</tr>


<tr>
<td class="org-left">extendleft(iterable)</td>
<td class="org-left">在左端批量添加元素(顺序反转)</td>
<td class="org-left">d.extendleft([1,2])</td>
</tr>


<tr>
<td class="org-left">rotate(n)</td>
<td class="org-left">向右旋转n步(负数向左)</td>
<td class="org-left">d.rotate(1)</td>
</tr>


<tr>
<td class="org-left">clear()</td>
<td class="org-left">清空队列</td>
<td class="org-left">d.clear()</td>
</tr>
</tbody>
</table>

这里需要强调的是关于extendleft和rotate的应用,我们用下面的示例代码来演示:

```python
# extendleft
d=deque([1,2,3,4])
d.extendleft([5,6])
print(d) # deque([6,5,1,2,3,4])
# rotate
d = deque([1, 2, 3, 4])
d.rotate(1)
print(d)  # deque([4, 1, 2, 3])
d.rotate(-2)
print(d)  # deque([2, 3, 4, 1])
```

<a id="org97dfeb8"></a>

## 2.5 List Comprehensions

列表推导式其实就是循环的一种高效写法,他可以视作将操作应用到序列中的每个元素来创建列表.

```python
x=[1,2,3,4,5]
square=[s*s for s in x] # 计算x每个元素的平方
```

不仅如此,还可以通过加if条件判断语句来过滤一些元素,如

```python
x=[1,-2,3,-4,5]
square=[s*s for s in x if s>0] # 计算x中每个正元素的平方
```

因此列表推导式的通用格式如下:

```python
[<expression> for <variable_name> in <sequence> if <condition>]
```

比较常见的应用如下:

1.  通过列表推导式收集特定的字典的值.

    ```python
    names=[stu['name'] for stu in classes]
    ```

2.  可以执行类似数据库的查找操作

    ```python
    height_name=[stu['name'] for stu in classes if (stu['height']>170)&&(stu['height']<180)]
    ```

3.  可以同时执行列表函数操作

    ```python
    total=sum([stu['scores'] for stu in classes])
    ```

类似与列表推导式,其实还存在如集合推导式和字典推导式,在这快速介绍一下,集合推导式的作用其实是可以用来去除一下重复的元素,字典推导式则是在集合推导式的基础上指定键值对映射.

```python
names={stu['name'] for stu in classes}
names_score={stu['name']:stu['scores'] for stu in classes}
```

<a id="orgb093176"></a>
