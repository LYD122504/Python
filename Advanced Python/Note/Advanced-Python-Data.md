---
title: Advanced Python-Data Handling
date: 2026-01-28 00:16:59
tags:
    - Python
categories: Advanced Python
mathjax: true
---


<a id="org3d97304"></a>

# Python Review

在之前Practical Python系列笔记中,我们只是简要介绍了一下数值型变量的运算符,在此我们介绍一下数值型变量的常用方法:

1.  浮点数的分数表示:as\_integer\_ratio

    ```python
    x.as_integer_ratio()
    a, b = x.as_integer_ratio()
    print(a / b)   # 可还原为原始浮点数
    ```

    其返回一个二元组(p,q),表示该浮点数的精确有理数表示x=p/q.

    <!--more-->

2.  判断是否为整数:is\_integer

    ```python
    x.is_integer()
    ```

    is\_integer()判断的是数值意义,与类型无关,这与我们之前常见的判断类型的不同,

    ```python
    x = 4.0
    x.is_integer()      # True
    isinstance(x, int) # False
    ```

    is\_integer是通过数值的角度判断是否为整数,而isinstance则是判断变量类型.

3.  int的有理数视角:numerator/denominator

    ```python
    y=12345
    y.numerator # 12345
    y.denominator # 1
    ```

    这是因为从数学角度来说,任意的整数本质上都是有理数.

4.  整数的二进制规模:bit\_length

    ```python
    y=12345
    y.bit_length
    ```

    他将会返回表示该整数所需的最少的二进制位数.其对应的数学计算公式为 $$ BitLength(y)=\lfloor \log_2(y)\rfloor+1 $$


<a id="org433e382"></a>

# Data Handling


<a id="orge3d9318"></a>

## Variations on Classes

\_\_slots\_\_是一种节省内存的类定义方式.普通的python类的实例都有一个\_\_dict\_\_属性,用于动态存储属性.这为python类的使用带来了变量的灵活性,但是为了维护这个字典属性,导致每个实例的内存开销比较大.我们使用\_\_slots\_\_显式声明,这个类只允许有哪些属性,从而不再为每个实例创建\_\_dict\_\_属性,限制实例属性的动态增加,显著减少内存占用.

```python
class Point:
    __slots__ = ('x', 'y')
    def __init__(self, x, y):
        self.x = x
        self.y = y
```

其优点在于节省内存(适合存储大量的小对象),访问属性更快(少了一层字典查找);缺点在于不能随意添加新的属性,多继承上会报错multiple bases have instance lay-out conflict,这是因为对于多继承需要将两个父类的slot合并成一个实例,但是他不能保证生成一个安全的内存布局,slot在子类的实例是固定的内存偏移,两个独立父类都声明slot会可能出现重叠或冲突的情况.

dataclass是用于减少样板代码的类.很多类从本质上来说就是只是数据容器,却要重复写\_\_init\_\_函数,这是一些重复的工作.因此dataclass使用声明式方式来描述字段,由解释器自动生成常用方法.

```python
from dataclass import dataclass
@dataclass
class Point:
    x:float
    y:float
```

这相当于就是手写了一个\_\_init\_\_的普通类.这个形式其实就是前面介绍过的装饰器,并且这个装饰器是可以传入参数的,常见的参数使用如下

```python
@dataclass(frozen=True, slots=True)
class Point:
    x: float
    y: float
```

frozen=True表示实例不可变,slots=True表示自动生成\_\_slots\_\_属性.但是需要注意的是,dataclass里声明的类型并不是强制执行的,也就是你就算输入的类型和他声明的不同,他也不会报错,也会正常运行.

```python
from dataclasses import dataclass
@dataclass
class Person:
    name: str
    age: int
    p = Person("Alice", "30")  # age 其实是 str，但 Python 不会报错
    print(p)#Person(name='Alice', age='30')
```

其优点是极大减少了模板代码,可读性强,更接近数学/结构化定义,与类型注解天然结合;缺点在于不适合逻辑非常复杂,生命周期管理重的对象

namedtuple虽然其归入到类的变体,但其实他和元组会更接近一点,他是一个不可变的具名的元组.普通的元组内存小,不可变,而且只能依靠索引访问,可读性差.namedtuple在此基础上增加了字段名,在保留tuple行为的同时,提高了代码的可读性.他的生成有两种不同的方式

```python
import typing
class Stock(typing.NamedTuple):
    name:str
    shares:int
    price:float
    from collections import namedtuple
    Stock = namedtuple('Stock',['name', 'shares', 'price'])
```

后者的第一个参数必须存在,他就是生成类的类名.他的最主要的特点就是不可变(线程安全,可以哈希化),内存占用小,以及支持解包,索引和迭代;他的缺点就是不能有可变字段,不适合复杂行为.


<a id="org7dac709"></a>

## Malloc Trace

tracemalloc用于跟踪程序运行中的内存分配,一般用于帮助找出内存泄露和内存使用热点,在调试大型程序,排查内存增长十分有效.其只会跟踪Python堆内存分配,不会跟踪C扩展直接分配的内存.主要特点是他可以记录每次内存分配的位置(文件+行号),可以对比不同时间点的内存分配变化,可以按文件,行号统计内存占用.

启动跟踪

```python
import tracemalloc
tracemalloc.start()
```

可选参数nframe:记录多少层调用堆栈,默认1.如果不是1,那么他就会检查当前函数以及(n-1)个函数栈内函数的内存分配.跟踪的内存是 Python 堆分配的对象.

获取当前内存快照

```python
snapshot = tracemalloc.take_snapshot()
```

snapshot包含当前所有Python对象的内存分配信息,返回的是一个tracemalloc.Snapshotd对象,可以按文件,行号,函数等统计.基于此查看内存使用

```python
top_stats = snapshot.statistics('lineno')  # 按行号统计
for stat in top_stats[:10]:  # 输出前 10 条
    print(stat)
```

里面的输出会有lineno表示代码的行号,size表示调用的内存大小,以及count为分配次数.对比两次快照,用于查看内存增长情况

```python
snapshot1 = tracemalloc.take_snapshot()
# 执行一些操作
my_list = [i for i in range(10000)]
snapshot2 = tracemalloc.take_snapshot()
top_stats = snapshot2.compare_to(snapshot1, 'lineno')  # 比较内存变化
for stat in top_stats[:10]:
    print(stat)
```

其会输出内存分配增长最多的前十个的代码行.

查看当前内存总占用

```python
print(tracemalloc.get_traced_memory())  # 返回 (当前跟踪内存, 峰值)
```

他返回的单位是字节,峰值可以用来帮助判断内存峰值的位置.

停止跟踪内存配置

```python
tracemalloc.stop()
```

停止跟踪Python堆内存分配,停止跟踪后再调用快照会报错.

常用的工程场景为

1.  找内存泄漏:运行程序一段实践,对比内存快照,看哪些行内存不断增长
2.  分析热点代码:哪些函数/文件分配内存最多,优化数据结构或算法
3.  调试大对象:快速定位大数组,字典等对象的来源

snapshot.filter\_traces(filters):过滤掉不关心的模块;Trace表示一次内存分配记录,而snapshot则是在某一时刻的所有trace的合集,这里面他会包含标准库,三方库以及自己代码的分配记录,通常这十分杂乱无章.这里的filter\_trace会保留或排除某些trace,并且生成一个新的snapshot.这里的filters是一个TracebackFilter对象的列表:

```python
tracemalloc.TracebackFilter(inclusive: bool,filename_pattern: str)
```

这里的inclusive的作用十分关键,True表示只保留匹配该模式的trace,False则是排除匹配该模式的trace.filename\_pattern则是一种glob风格的路径匹配字符串,这个glob风格的主要特征其实就是我们前面提到的模糊查找,用通配符匹配字符串,常用的例子为

```shell
'*'
"*/site-packages/*"
"*/lib/python3.11/*"
"*/your_project/*"
```

例如我们将标准库和三方库的内存分配舍弃,只看自己的代码分配

```python
import tracemalloc
snapshot = tracemalloc.take_snapshot()
filters = [
    #过滤 Python 导入系统内部产生的内存分配记录
    tracemalloc.TracebackFilter(False, "<frozen importlib._bootstrap>"),
    #过滤 tracemalloc 无法追溯到 Python 源文件的内存分配
    tracemalloc.TracebackFilter(False, "<unknown>"),
    tracemalloc.TracebackFilter(False, "*/lib/python*/*"),
    tracemalloc.TracebackFilter(False, "*/site-packages/*"),
]
snapshot = snapshot.filter_traces(filters)
```

只看某个模块/文件夹的内存

```python
snapshot = snapshot.filter_traces([
    tracemalloc.TracebackFilter(True, "*/myproject/*")
])
```

snapshot中只包含myproject目录下产生的内存分配.


<a id="orge9ffd9c"></a>

## Memory Comparsion

我们用不同的方式读取同一个csv文件并且用tracemalloc测量了内存使用情况.为了简便起见,我们不贴完整的代码,只是做简要的结果分析.

首先,用如下的代码来将文件直接读取成一个字符串,

```python
data=f.read()
```

内存消耗约12.36MB,只读取原始字符串,没有任何解析,也没有创建额外对象,这是最为节省内存的方式,仅需要存储文本内容,这样只能做字符串处理,不需要做结构化访问.

用如下的代码来将文件按行读取成字符串列表,

```python
data=f.readlines()
```

内存约为40.73MB,这一过程创建了约57万条str对象和一个存储这些对象的列表.但我们发现他的内存显著高于前一个方法,这是因为Python的字符串对象有额外的开销,因为每个str都是一个对象,包含元数据,因此他比直接存储需要消耗更多的内存空间.

用如下的代码来将文件读取成元组列表,

```python
records.append((row[0], row[1], row[2], int(row[3])))
```

内存约为114.73MB,这个时候每行已经从一个字符串对象变成了4个元素的tuple,每个元组中有三个字符串对象和一个整数对象,每个tuple仍然是独立对象.因此他每一行其实被存储在1个tuple对象,3个字符串对象和1个整数对象中,故而其会比读取字符串列表有明显的内存消耗提升.

用如下的代码来看将文件读取成一个字典列表,

```python
records.append({headings[0]:row[0],headings[1]:row[1],headings[2]:row[2],headings[3]:int(row[3])})
```

内存约179.42MB.字典是最为占用内存的常见容器之一,每个字典都有自己的哈希表,即使只有四个key也会在分配空间时预留空间,稀疏结构存储.key是字符串,value是字符串+int.因此他的内存效率低但是他的访问十分灵活

用如下的代码做一个自定义类列表读取,

```python
class Row:
    def __init__(self, route, date, daytype, rides):
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = rides
for row in rows:
    records.append(Row(row[0],row[1],row[2],int(row[3])))
```

内存约128.59MB.类存储虽然也是使用的\_\_dict\_\_来做存储本质上也是一个字典,但是由于每个实例字段名完全一样且内存分布一致,因此Python会自动复用相同的字符串和整数对象,故而总对象数更少,间接的降低内存.dict为速度牺牲空间,类在值复用且结构一致下更省.

用如下代码将文件用namedtuple的方式存储,

```python
Row=namedtuple('Row',['route','date','daytype','rides'])
```

内存约为119.36MB.namedtuple本质上是tuple的子类,但支持使用字段名访问.由于他的底层实现还是基于元组完成的,因此他的内存比普通的class更省.而且每个实例都没有\_\_dict\_\_字典,属性通过索引访问,开销接近普通tuple.

用如下的代码将文件用使用\_\_slots\_\_的类

```python
class Rows:
    __slots__ = ['route', 'date', 'daytype', 'rides']
```

内存约110.11MB.\_\_slots\_\_禁用了\_\_dict\_\_属性,将实例属性直接存储在固定数组里面,减少了内存碎片和对象开销.


<a id="org5fc6b6c"></a>

## Collection Module

defaultdict主要是用来做一对多映射问题的,Counter则是一个计数器,并且他提供了排序的功能.我们将两个对象组合在同一个代码中简要介绍一下,

```python
dict_year_routes=defaultdict(Counter)
for r in rows:
    year=r['date'].split('/')[2]
    dict_year_routes[year][r['route']]+=r['rides']
    differ=dict_year_routes['2011']-dict_year_routes['2001']
    print(differ.most_common(5))
```

这里的代码创建了一个默认类型为Counter的defaultdict类.我们通过dict\_year\_routes[name]的方式访问的是一个Counter对象,其内部仍有一个字典形式,因此需要再做一次索引才可以到达计数的功能.最后的differ是两个计数器类的作差,其实就是其中每个键的计数作差,但是只保留结果为正数.

```python
from collections import Counter
c1 = Counter(a=5, b=3, c=2)
c2 = Counter(a=2, b=4, d=1)
result = c1 - c2
# 等价于：
# a: 5 - 2 = 3 → 保留
# b: 3 - 4 = -1 → 舍弃（不保留 ≤ 0 的值）
# c: 2 - 0 = 2 → 保留
# d: 0 - 1 = -1 → 舍弃
```

deque则是一个双端队列,因此他主要是处理队列相关的问题,例如他可以用来存储最后N个对象的历史.

```python
history=deque(maxlen=3)
with open('../Data/ctabus.csv','r') as f:
    for line in f:
        history.append(line.strip())
        print('Last 3 lines in the file:')
for record in history:
    print(record)
```

ChainMap用于将多个字典组合成一个单一的,可更新的视图,而不需要实际的合并他们.在需要按优先级顺序多个作用域(如配置,环境变量,默认值)时,传统做法是层层嵌套

```python
if key in dict
```

或者手动合并字典.但这样的话,合并会复制已有的数据,浪费内存;无法动态反应底层字典的变化;出现了逻辑冗余.ChainMap提供了一个轻量级的视图,按顺序搜索键,并且支持写操作,默认写入第一个映射.

```python
from collections import ChainMap
defaults = {'color': 'red', 'user': 'guest'}
env_vars = {'user': 'alice'}
cli_args = {'color': 'blue'}
# 组合：优先级从高到低(cli_args>env_vars>defaults)
config = ChainMap(cli_args, env_vars, defaults)
print(config['user'])
print(config['color'])
config['debug'] = True
print(cli_args)
```

这里的debug键对会直接写入cli\_args,也就是第一个字典映射.ChainMap的主要特性是

1.  查找顺序:从左到右搜索,第一个匹配的键生效
2.  写/删操作:默认作用在第一个映射(如果想要修改可以通过子类重写的方式)
3.  动态性: 底层的字典变化可以直接反映到ChainMap里面
4.  不复制数据:内存开销极小(仅存储对原字典的引用)

常用的方法是.maps返回底层字典列表(可以进行修改,其修改会直接影响到ChainMap的结果);.new\_child()在底层字典列表前面添加一个新的空字典,常用于作用域压栈,他会返回一个新的ChainMap,不是对原有ChainMap的就地操作;.parents返回除第一个外的所有映射,类似弹出顶层作用域.

这里需要注意的是ChainMap不是字典的替代品,而是多字典联合查找的工具.如果你需要合并所有的字典键对,那你需要做一些手动合并操作,对于某些只读场景,其实Python3.8以上提供的dict|dict操作符可能也是不错的选择,但是他并不支持动态更新.

```python
d1 = {'a': 1, 'b': 2}
d2 = {'b': 3, 'c': 4}
merged = d1 | d2
print(merged)  # {'a': 1, 'b': 3, 'c': 4}
# 上面体现出了合并的时候相同变量名的右边优先级更高
# Python3.9以上则提供了就地操作符
merged|=d1
print(merged)
```


<a id="org87b88c6"></a>

## Iteration

在遍历一个可迭代对象时,如果我们只关心循环次数或者某种元素的变化,而对对象里的其他部分不感兴趣,那我们可以用下划线作为占位符来表示我并不关心这个数值.

```python
for _ in range(5):
    print('Hello')
```

其实下划线是一个合理的变量名,只是按照通用的惯例而言,我们会默认这个值是被抛弃的.但是他仍然会占用内存,只是提醒程序员这个值并不会被使用.

通配符解包:Python中引入了\*用于解包多个元素,常用于抓取剩余项.

```python
a,*rest,b=[1,2,3,4,5]
print(a,rest,b)# 1 [2,3,4] 5
```

中间的解包元素会捕获中间所有没有显式分配的元素.这样的解包只能出现一次.当然我们也可以与上面的下划线合并形成的丢弃不需要的没有显式分配的元素.

```python
first,*_,end=[1,2,3,4,5]
print(first,end) # 1 5
```

解包可迭代对象,使用\*或直接赋值来将可迭代对象(如列表,元组)的元素分配给多个变量.

```python
x,y,z=[1,2,3]
def f(a, b, c):
    return a + b + c
args = [1, 2, 3]
f(*args)  # 等价于 f(1, 2, 3)
```

他比我们常用的+更好一点,因为+要求操作数同类型且支持拼接的序列(如list+list),如果用的如list+tuple的情况,那么如果用加号就会报错,但可以用解包符来提取元素.

解包字典,使用\*\*来将字典解包为关键字参数

```python
def greet(name, age):
    print(f"Hello {name}, you are {age} years old.")

info = {'name': 'Alice', 'age': 30}
greet(**info)  # 等价于 greet(name='Alice', age=30)
```

解包符也可以应用在函数参数里面,因为Python的函数只需要满足位置参数放在关键字参数(默认参数)之前,各种参数类型的组合就是合法的.

```python
def func(pos1,pos2,...,default1=..,default2=...,)
a=(1,2,3)
b={'c':3,'d'=4}
func(1,*a,**b,flag=1)
```

生成器是一种惰性求值迭代器,他在遍历的时候逐个产生值,不会保存已生成的值.一旦遍历完成就不能够从头开始.

```python
gen = (x**2 for x in range(3))  # 生成器表达式
list(gen)  # [0, 1, 4]
list(gen)  # [] —— 已耗尽，无法再次使用
```

如果我们需要多次使用的话就应该将其转换为列表或者重新创建生成器.这是因为生成器内部维护一个状态(当前执行到哪一步),一旦结束(抛出StopIteration),状态就终止了.


<a id="orge913d96"></a>

## Builtin

内置类型(Builtin types)是Python解释器原生支持的对象类型,如int,float等.他们几乎都是基于C语言编写的,直接写入Cpython解释器内部.这些内置类型是最为基础的,最为高效的对象类型.换言之,如果我们声明一个内置类型对象,其实是创建了一个由C结构体表示的,高度优化的底层对象.

无论是否为内置类型,每个Python对象在内存中都包含三个基本字段:

1.  id为对象的唯一标识,实际上是他在内存中的逻辑地址,利用id(object)读取.
2.  class为对象的类型,利用type(object)读取,决定了它有哪些方法和属性
3.  refcount为引用计数,用于垃圾回收(当计数归零时,对象会被释放)

```python
a=[1,2]
b=a # refcount+=1
c=[a,None] # refcount+=1 again
```

上面的这个结构是对所有对象都是通用的,但是内置类型的字段会更加紧凑,访问速度更快,因为他的底层设计是C语言的结构体,而不是动态字典.

![2026-01-24_00-28-57_screenshot](https://github.com/LYD122504/picx-images-hosting/raw/master/20260128/2026-01-24_00-28-57_screenshot.7pss8cyl2.png)

简要介绍一下内置类型的内部表示和内存开销:

1.  None是一个单例对象,全局只有一个None实例.内存结构也是十分简单的,没有数据字段,只有对象头.因此他的内存占用极小,但仍然有基础的内存开销.

    ![2026-01-24_13-45-06_screenshot](https://github.com/LYD122504/picx-images-hosting/raw/master/20260128/2026-01-24_13-45-06_screenshot.60ur1j0etz.png)

2.  float是64位双精度浮点数类型,其内存总大小是24字节(在64位系统上).其中class指针占用8字节,refcount占用8字节,value也会占用8字节.其验证代码如下:

    ```python
    import sys
    print(sys.getsizeof(2.3))
    ```

    ![2026-01-24_13-51-11_screenshot](https://github.com/LYD122504/picx-images-hosting/raw/master/20260128/2026-01-24_13-51-11_screenshot.5mobans3yw.png)

3.  int类型表示任意精度整数,他并非是C/C++那样的固定内存32位或64位.其中class指针占用8字节,refcount占用8字节,size表示有多少个digit块,占用8个字节,真正的存储位置在digit列表里面,每个元素都是4个字节.但是存储数据的32位中我们需要提供两个位次来做进位或上下溢判定,因此我们只有30位用于存储数据.其验证代码如下:

    ```python
    import sys
    print(sys.getsizeof(0)) #28
    print(sys.getsizeof(2**30)) #32
    print(sys.getsizeof(2**60)) #36
    print(sys.getsizeof(2**90)) #40
    ```

因此,从上面的运行看,python内置的int类型看,会随着数值的增大,digits数组变长,从而导致内存线性增长.

![2026-01-24_20-50-08_screenshot](https://github.com/LYD122504/picx-images-hosting/raw/master/20260128/2026-01-24_20-50-08_screenshot.mkwsqt5l.png)

1.  str则是python的字符串类型.我们主要介绍一些独有的字段属性.length存储的是字符串中字符的数量,并不是字节数,这样可以使得我们在查询长度的时候时间复杂度降为O(1),对于大量查询字符串长度的程序具有极高的优化.hash属性卡会存储字符串的hash值,因为对于Python而言,字符串一般是用作字典的键或集合的元素.这些数据结构需要依赖对象的哈希值来实现:快速查找,去重和等价判断.他可以存储hash值是因为字符串是一个不可变对象,故而生成一次hash值,他的hash值就不会有任何变化.她会在首次调用或用作dict/set的键时计算,Python会计算hash值并存储以后的调用都是O(1).flags是一种标志位,用于记录字符串的编码格式和状态,用于实现自适应字符串表示.如ASCII表示一个字符一个字节,Latin-1表示一个字符两个字节,USC-2/USC-4表示一个字符两个或四个字符.data则是实际的字符数据,他可以按需选择字符宽度,并以\x00结尾,便于和C函数交互.

    ```python
    import sys
    print(sys.getsizeof('n')) # 1 ASCII char → 1B data + overhea
    print(sys.getsizeof('ñ')) # 1 Latin-1 char → 2B data + overhead = 74B
    ```

![2026-01-24_21-59-13_screenshot](https://github.com/LYD122504/picx-images-hosting/raw/master/20260128/2026-01-24_21-59-13_screenshot.491s6mh1y2.png) Python对象有显著的固定内存开销.频繁创建小对象(如解析大量文本生成无数短字符串)会导致高内存消耗.

内置类型通过设置对象协议来实现某些功能.Python的运算符和内置函数是通过特殊方法实现的,这些方法构成协议.

```python
a=2
b=3
print(a+b) # 相等于a.__add__(b)
print('hello') # 等价于"hello".__len__()
```

协议是解释器的硬编码行为.字节码直接调用协议方法,可以用dis模块查看编译后的字节码,如下所示

```python
import dis
def bar(x,y):
    return x+y
print(dis.dis(bar)
'''
 25           0 RESUME                   0

 26           2 LOAD_FAST                0 (x)
              4 LOAD_FAST                1 (y)
              6 BINARY_OP                0 (+)
             10 RETURN_VALUE
None
'''
```

RESUME 0是Python3.11引入的一个帧初始化指令,用于职场更快快的函数调用和生成器恢复.他对协议机制并不会有什么太大的影响.LOAD\_FAST是将局部变量压入求值栈.BINARY\_OP是Python3.11的通用二元操作指令,他会触发对象的\_\_add\_\_协议.

我们可以自定义一些自己的内置类型,并且实现一些协议,让自定义内置类型可以表现十分自然.

```python
from functools import total_ordering

@total_ordering
class MutInt:
    __slots__=['value']
    # Mutable Integers
    def __init__(self,value=0):
        self.value=value
    # Fixing output
    def __str__(self):
        return str(self.value)
    # !r的作用是在f-string中调用repr()
    # !s的作用是在f-string中调用str()
    # !a的作用是在f-string中调用ascii()
    def __repr__(self):
        return f'MutInt({self.value!r})'
    # 用于f-string,string.format()做格式化自动调用
    def __format__(self,fmt):
        return format(self.value,fmt)
    # Math Operator
    def __add__(self,other):
        if isinstance(other,MutInt):
            return MutInt(self.value+other.value)
        if isinstance(other,int):
            return MutInt(self.value+other)
        else:
            raise NotImplemented

    __radd__=__add__# Reversed operands

    def __iadd__(self,other):
        if isinstance(other,int):
            self.value+=other
            return self
        if isinstance(other,MutInt):
            self.value+=other.value
            return self
        else:
            raise NotImplemented
    # Comparisons
    def __eq__(self,other):
        if isinstance(other,int):
            return self.value==other
        if isinstance(other,MutInt):
            return self.value==other.value
        else:
            raise NotImplemented
    def __lt__(self,other):
        if isinstance(other,int):
            return self.value<other
        if isinstance(other,MutInt):
            return self.value<other.value
        else:
            raise NotImplemented
    # Coversions
    def __int__(self):
        return self.value
    def __float__(self):
        return float(self.value)
    __index__=__int__
```

我们需要解释一下上面的代码.\_\_format\_\_函数是用于f-string,string.format()做格式化自动调用.\_\_add\_\_函数只能够支持作为加法的左操作数,为了满足加法交换律,我们重新定义了\_\_radd\_\_函数,程序如果没有找到合适的加法函数,会自动调用radd函数.但是这样只能够覆盖加法的操作,如果我们希望考虑加法的就地操作,那么需要实现\_\_idd\_\_函数.对于逻辑对比关系,我们需要实现如\_\_eq\_\_函数来判断相等,\_\_lt\_\_函数来判断小于.但是如果我们对每个逻辑判断关系都去写,那会是十分冗余的,因此引入functools模块的total\_ordering装饰器,他可以让我们只实现一个关系比较,从而自动补全其余的.我们同样可以为自定义内置类型可做一个类型转换函数,但是需要注意的是,如果只是设置了类型转换函数,他并不能在索引中自动转换为合适类型,需要手动操作,但可以重定义\_\_index\_\_函数.


<a id="org887194c"></a>

## Container Representation

和C/C++不同的是,Python的容器只会存储值的引用,而不是值本身.因此容器的操作实际上也是操作引用,而不是操作对象.对于Python中的可变容器而言,如list,dict和set,他不是按照需要分配恰好的内存,而是会过度分配(over-allocation),这是为了方便append和insertion操作加速.如果我们提前分配了额外的空间,那么append操作会十分快,因为空间已经准备好了,不需要重新向系统请求分配空间.

容器内存的增长行为:容器的使用内存的增长会是现使用内存的某种比例.

1.  List的内存增长方式是当内存占用满了,会增加现有内存的约12.5%,并非固定倍数.其测试代码如下所示,

    ```python
    a=[]
    print(sys.getsizeof(a))
       for i in range(10):
           a.append(i)
           print(a,sys.getsizeof(a))
           # empty 56; [0,1,2,3] 88
           # [0:4] 120; [0:9] 184
    ```

空列表会消耗56个字节,如果加入一个数字会消耗88个字节,此时开辟了32个字节的空间,相当于四个位置;一直等到存储完四个位置,开始存储第五个位置的时候,列表会请求增加内存空间,将88个字节扩充到120个字节,同样允许继续存储四个位置,一直到存储到第八个位置,开始存储第九个位置的时候,列表会继续请求增加内存空间,将120扩充到164个字节,也就是允许继续存储8个字节.这里我们需要声明的是,引用需要占用8个字节是因为所使用的电脑是64位的,如果用的32位系统则是4个字节.

1.  Set的内存增长方式是当存储元素占用了开辟空间的2/3,就会将开辟空间增长4倍.但是电脑上测试出来,他的增加阈值应该是3/5,具体可能需要查阅python相应版本的底层设计.

    ```python
    a=set()
    print(sys.getsizeof(a))
       for i in range(20):
           a.add(i)
           print(a,sys.getsizeof(a))
           # empty 216; {0,1,2,3} 216
           # {0,...,4} 728; {0,...,18} 2264
    ```

2.  Dict的内存增长方式是当存储元素占用了开辟空间的2/3,就会将开辟空间增长2倍.

    ```python
    a={}
    print(sys.getsizeof(a))
    for i in range(20):
        a[i]=i+1
        print(a,sys.getsizeof(a))
    # 第6个元素扩容 第11个元素扩容
    ```

    这里的逻辑是初始是8个空间,其空间的2/3并向下取整是5,也就是当存储空间使用了5个元素,添加第6个元素的时候需要重新开辟空间,其增长为两倍,所以会开辟至16个空间,其空间的2/3并向下取整是10,因此第11个元素才会重新开辟新的空间.

字典和集合的使用中会经常需要做键值查找,因此他们的底层实现都是基于Hash表完成的,这是因为Hash表的查找是O(1)时间复杂度的.因此我们需要介绍一下关于集合和字典的哈希化.字典和集合的键通过使用\_\_hash\_\_函数获得其hash值,并存储起来,在程序内部使用.因此这要求字典和集合的键值必须是可以哈希化的对象,也就是字符串,数字或者元组.而列表,集合和字典等不能被用于哈希化,故而不能成为字典和集合的键值.如果我们需要自定义一个数据类型,并希望他可以成为字典或集合的键值,我们需要实现\_\_hash\_\_()方法和\_\_eq\_\_()方法,其中hash方法是为了保证类型可以哈希化,而eq方法则是保证相同数值的哈希值一样,虽然不会妨碍使用,但是如果没有他那么可能会出现同一个值有不同的哈希值,这与哈希化的初衷相悖.

在此简要介绍一下字典的内部布局.我们向程序输入一个字典, 系统会计算字典键值的hash值,并依据这些hash值将entiries数组的引用存储到hash表的相应位置上,entries数组会存储相应的键值对.如果我们要查找某个键值对,其实就是上面过程的逆向,因此不在此赘述.这里其实就会出现一个很自然的问题,也就是哈希冲突问题,当hash表不断被填充的时候,发生原有的位置被占据了的情况是十分常见的,因此我们需要一个解决冲突的算法来除了这个问题.Python中引入了一个扰动寻址法的方式来处理哈希冲突问题,其代码如下,

```python
# 初始位置
mask = table_size - 1
i = hash(key) & mask
# 冲突后迭代探测
perturb = hash(key);  # perturb 初始为完整哈希值
do {
    i = (i * 5 + perturb + 1) & mask
    PERTURB_SHIFT = 5
    perturb >>= PERTURB_SHIFT 
} while (冲突);
```

这个算法结合了线性项(i\*5+1)提供基础的伪随机探测序列,并加上了扰动项perturb,将Hash值的高位引入探测过程.我们常见的探测序列其实并没有扰动项,添加扰动项则是可以解决低位聚集问题.哈希表索引通常使用的hash&mask计算,他只使用哈希值的低位.当多个键的低位相同的时候,尽管高位可能有很大的差异,他们还是会聚集在表的某个区域,导致线性探测容易继续陷入局部聚集,并重复访问已知冲突区域,降低匹配效率.扰动策略是逐步将哈希值的高位引入探测序列,这样探测序列会受哈希值的每一位,极大降低冲突的概率.

这里我们发现他的求余运算是通过按位取和运算实现的,这是因为我们一般设定哈希表的长度为2的幂次.对于任意一个整数,我们都可以将其写成一个唯一的二进制形式, 
$$
 h=\sum_{k=0}^{m}a_k2^k=\sum_{k=0}^{n-1}a_k2^k+\sum_{i=n}^ma_i2^i 
$$
 因此,h对哈希表长度$2^n$取余得到的结果其实就是最后n-1位二进制的值.而如果我们考虑的是与哈希表长度减一按位取和操作,因为哈希表的长度为$2^n$,那么长度减一的二进制形式其实就是最后n-1个二进制位为1,其余位置为0,按位取和其实得到的结果就是原有整数的二进制的后n-1位二进制的值,这与取余操作是一样的,因此我们可以将两个运算替换使用.

和上一小节一样,我们也可以自定义容器类,只需要设置好必须的协议方法.如果我们需要创建一些新的容器,我们可以使用collections.abc中定义的抽象基类.常用的抽象基类如下所示,

| 抽象基类        | 必须实现的方法                     |
| --------------- | ---------------------------------- |
| Container       | contains(用于支持in操作)           |
| Iterable        | iter(支持for循环)                  |
| Iterator        | iter,next(自定义迭代器)            |
| Sequence        | getitem,len                        |
| MutableSequence | getitem,len,setitem,delitem,insert |
| Mapping         | getitem,iter,len                   |
| MutableMapping  | getitem,iter,len,setitem,delitem   |
| Set             | contains,iter,len                  |
| MutableSet      | contains,iter,len,add,discard      |


<a id="org8b70703"></a>

## Assignment

Python的许多操作很多都是基于赋值操作的.与C/C++不同的是,Python的赋值操作并不会复制被赋值的值的副本,因此所有赋值都只是复制被赋值的值的引用.所以赋值操作会导致多数变量指向同一个元素.我们修改其中一个变量,会使得全部变量的数值都发生修改,因此在修改变量的时候需要谨慎检查引用.同样函数调用参数其实也是以引用的形式传入,而不是传入值,所以参数在函数内部的变化是可以影响到外部的.需要注意的是,Python中许多对象类型是不可变的.

虽然上面提出Python的赋值操作是赋值引用副本,但如果我们对他进行重赋值并不会影响原有的引用赋值副本,而是指向了另一个存储空间.is操作符可以用于检测两个变量是否指向同一个地址.

```python
a=[1,2,3]
b=a
print(a is b)
```

而所有的对象都是具有自己独特的整数标识码,这种标识码可以用id函数读取.

```python
print(id(a))
print(id(b))
```

上面我们介绍了Python赋值操作的一些易错点,因此我们简要介绍一下不可变对象的优点.不可变对象可以安全地共享数据并不用担心数值被修改;由于其不可变性,共享可以节省相当多的内存.

容器中提供了一些方法来做复制操作,如

```python
a=[2,3,[100,101],4]
b=list(a) # make a copy
print(a is b) #False
```

然而,他只保证了外层容器的独立性,对于内层容器,依旧是指向相同的地址.

```python
# shallow copies
a=[2,3,[100,101],4]
b=list(a)
print(a is b) # false
print(a[1] is b[1]) # false
print(a[2] is b[2]) # true
```

如果我们需要完全复制某个对象以及其中的所有元素,那么可以选择使用copy模块的deepcopy函数.这也是唯一安全的方式来复制变量.
