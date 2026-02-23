---
title: Advanced Python-Function
date: 2026-02-23 16:22:11
tags:
    - Python
categories: Advanced Python
mathjax: true
---

# Functions


<a id="orgdaca2da"></a>

## Function Arguments

函数是程序的基本构建单元,如模块的顶层函数,类的方法.程序的几乎所有代码应该封装在函数中.Python函数的设计原则,我们希望函数是自包含的(self-contained),仅操作输入的参数.

<!--more-->

<center><img src="https://github.com/LYD122504/picx-images-hosting/raw/master/20260223/2026-02-13_12-18-53_screenshot.51eoqh0bcs.png" style="zoom:75%;" /> </center>

如果输入相同的参数,则应返回相同的结果,这也就是所谓的函数可预测性.我们在编写程序中需要尽可能避免潜在的副作用,其核心目标是简洁性和可预测性.

函数名和函数参数都是对外的调用接口.调用函数的形式应该直观易用,这是设计良好API的关键.同时我们也可以进一步声明一下函数的命名规范,推荐采用小写字母和下划线的方式来命名函数,而不应采用驼峰命名法,如

```python
def read_data(filename):
    pass
```

而一般用于\_引导的函数名来指示这个函数是内部或私有函数,如

```python
def _internal_func():
    pass
```

在程序运行中,函数可能需要设置默认参数,如

```python
def read_data(filename,debug=False):
    pass
```

若默认参数已被设置,则在函数调用的时候,可以选择输入相应参数.就算不输入,函数也会基于默认参数进行函数流程.需要强调的是,默认参数必须在函数参数定义的最后位置.这里我们推荐采用关键字参数来设置可选参数,使用关键字参数传参会使代码可读性提升,我们可以用\*来强制使之后的参数调用.同时对于默认参数而言,我们需要尽可能不要用可变类型做默认参数,因为默认参数整个程序只会创建一次,因此程序会有粘性,即存在不可知的修改,

```python
def func(a,items=[]):
    items.append(a)
    return items
print(func.__defaults__)
print(func(1))
print(func.__defaults__)
print(func(2))
print(func.__defaults__)
```

默认参数会存放在函数的\_\_defaults\_\_属性中,如果默认参数可变的话,那函数的\_\_defaults\_\_属性中就会不断地记录之前的修改,而我们应该采用不可变值,如None,True,False,numbers或strings.如果默认参数是不可变值,那么默认参数在不断调用中保持原值.

```python
def func(a, items=None):
    if items is None:
        items = []
    items.append(a)
    return items
print(func.__defaults__)
print(func(1))
print(func.__defaults__)
print(func(2))
print(func.__defaults__)
```

用不可变的属性可以避免可变类型带来的意外改变.一般来说,可选值用None来表示该参数并未赋值,但需要注意的是,要对是否赋值做错误判断,不然容易报错.函数的设计需要能够接受抽象接口(如可迭代对象),这样会比绑定具体类型(如文件名)更具扩展性.我们也可以采用三个引号包括的字符串作为文档字符串,可以用help函数来查看,是良好的文档实践.我们可以用冒号来引导函数参数的希望类型,用->来引导返回值希望类型.但是这些符号的作用只是辅助代码检查器,IDE和文档生成,Python程序并不会在运行时强制类型检查.


<a id="org155b7e6"></a>

## Returning Value

函数应该清晰的返回相应值,若需要返回多个值,那么我们需要采用元组的方式进行,调用方则可以用多重赋值的方式解包.

```python
def divide(x,y):
    quotient=x//y
    remainder=x%y
    return(quotient,remainder)
print(divide(8,3))
q,r=divide(8,3)
print(q,r)
```

函数的返回值应该是可选的,常见的约定方式是None,这是正常的情况,只是返回的结果不存在;如果发生程序中的错误,则需要抛出异常.我们不应该滥用None来代替异常处理,调用方需要显式检查返回值是否为None,避免出现AttributeErrror异常.

Python提供了允许函数并发执行的方式(通过线程完成),而且多个函数在同一个解释器中并发运行,共享状态.

```python
from threading import Thread
import threading, time
def task(name):
    print(f"[{name}] start @ {time.time():.2f}")
    time.sleep(1)          # 模拟 I/O（如网络、磁盘）
    print(f"[{name}] end   @ {time.time():.2f}")
# 顺序执行（2秒）
start = time.time()
task("A"); task("B")
print(f"Sequential: {time.time() - start:.2f}s")
# 并发执行（≈1秒）
start = time.time()
t1 = threading.Thread(target=task, args=("A",))
t2 = threading.Thread(target=task, args=("B",))
t1.start(); t2.start()
t1.join(); t2.join()
print(f"Concurrent: {time.time() - start:.2f}s")
```

顺序执行的流程就是简单的完成一个函数之后再调用另一个函数,因此需要执行2s才能够完成执行流程.其关键在于只有一个线程(主线程),任务必须等前一个完成之后才能开始,资源利用率很低.并发执行的流程中,我们调用了time.sleep(1)用于模拟I/O操作,线程在此会释放GIL,允许其他线程运行.我们简要的解释一下流程,线程A,B同时被激发,线程A先抢到GIL,完成输出语句,遇到time.sleep(1)阻塞,操作系统将GIL让给线程B完成,同时完成输出语句后,遇到time.sleep(1)阻塞,等二者阻塞完成,再重新分配GIL完成输出,只是这个分配过程时间很短,可以几乎认为是同步的.

Python的threading模块支持多线程并发,其中的Thread是相应的线程类,其调用的语法结构,

```python
from threading import Thread
Thread(target=func,args=(name,)
```

target用来指定线程执行的函数,不需要加括号,只是传递函数本身,而不是做函数调用.args用来指定传递给目标函数的参数,其必须是元组,如果是单元素就需要加逗号,此时会返回一个未启动的线程对象,此时线程处于新建状态,并没有占用系统资源.start函数表示真正启动线程,其状态会从新建改为就绪而后运行,依靠操作系统来调度.其关键特性在于非阻塞调用且每个线程对象只能start一次.阻塞调用指的是调用后当前线程暂停一直到操作完成完成才继续执行;非阻塞调用指的是调用后立即返回,当前线程可以继续做其他的事情.

```python
print("开始")
t1 = Thread(target=task, args=("A",))
t1.start()  # ← 非阻塞：立即返回！
print("继续执行其他代码")  # 这行会立刻执行，不等 task 完成
```

不用run函数的原因是如果调用run则会在主线程中直接调用函数,不会创建新线程,从而失去并发意义.为了让主线程等待线程完成,使用join函数阻塞主线程,直到目标线程执行完毕,其相应的语法结构如下

```python
join(timeout=5)
```

其中的可选参数timeout表示最多等timeout秒,超时后主线程继续,但子线程依然在后台运行.

我们继续介绍一些关于并发执行的易错点.下面的代码将展示共享状态和竞态条件,

```python
counter = 0
num_threads = 100
def unsafe_increment():
    global counter
    for _ in range(10000):          # 增加次数
        current = counter           # 1. 读
        time.sleep(0)               # 2. 强制线程切换点（关键！）
        current += 1                # 3. 改
        counter = current           # 4. 写
threads = [threading.Thread(target=unsafe_increment) for _ in range(num_threads)]
for t in threads: t.start()
for t in threads: t.join()
expected = num_threads * 10000
print(f"Expected: {expected}") # 1000000
print(f"Actual  : {counter}") # 10563
print(f"Lost    : {expected - counter}
```

其根本原因是counter+=1被拆成了四步非原子操作,线程切换发生在中间的步骤,从而导致多个线程覆盖彼此的修改.我们以两个线程A,B为例,假设初始counter=0,A先读取counter为0存储在current,遇到暂停让出CPU;B同时也读取了一个counter为0存储在current,遇到暂停让出CPU;A恢复执行后current+=1,current变为1,同时counter=current=1;B重新恢复执行流程一样,所以两次自增却会丢失一次自加.这里我们用time.sleep(0)来强制当前线程主动让出CPU,从而提高线程在读写改过程中中间被切换的概率,从而使得竞态条件百分百可复现.原子操作指的是不可分割的操作:要么完全执行,要么完全不执行,中间不会被线程切换打断;非原子操作指的是可分割的操作:由多步组成,执行中途可能被其他线程打断.

为了避免上面的竞态条件,我们可以引入锁的概念

```python
counter = 0
lock = threading.Lock()
num_threads = 100
def safe_increment():
    global counter
    for _ in range(10000):
        with lock:       # 串行化临界区
            counter += 1
threads = [threading.Thread(target=safe_increment) for _ in range(num_threads)]
for t in threads: t.start()
for t in threads: t.join()
print(f"With lock: {counter}")  # 稳定输出 100000
```

锁会保护共享状态,保证临界区(修改共享数据的代码)同一时刻只有一个线程在执行.with lock语句则是会自动加锁和释放锁,从而避免死锁.wit lock的行为是尝试获取锁,如果成功就进入临界区,如果失败则会阻塞等待;在临界区内的代码,就会独占执行,其他的线程无法进入;退出with块,自动释放锁,等待队列中一个线程被唤醒获取锁.所以这样使得counter+=1在逻辑上完成原子化不可分割.整个程序的执行方式变为临界区串行和非临界区并发的方式,锁包裹的语句导致形成逻辑原子,不可拆分,仅在锁释放后才可以转换;他的运行性能较差,但是正确性没问题.加锁的性能消耗主要在临界区的串行化和频繁的锁竞争开销,因此锁适用于临界区较大且竞争不激烈的场景,如果我们以高频小操作为主,应该优先考虑无锁算法.

上面提到的threading模块支持的多线程并发,能够使I/O密集型场景(如网络请求,文件读写)完成并发执行,但是对于CPU密集型任务是无法实现的.因为会受到GIL(全局解释器锁)的限制,线程会在I/O时释放GIL,可以分配给其他线程,并发执行;而如果是CPU任务,则线程会持续占用GIL,无法并发执行.GIL指的是CPython中同一时刻中仅一个线程执行字节码.示例代码如下:

```python
def cpu_bound(n):
    while n > 0: n -= 1  # 纯计算，不释放 GIL
# 单线程
start = time.time()
cpu_bound(50_000_000)
print(f"Single thread: {time.time() - start:.2f}s")
# 双线程（受 GIL 限制）
start = time.time()
t1 = threading.Thread(target=cpu_bound, args=(25_000_000,))
t2 = threading.Thread(target=cpu_bound, args=(25_000_000,))
t1.start(); t2.start(); t1.join(); t2.join()
print(f"Two threads  : {time.time() - start:.2f}s")
def io_task():
    time.sleep(1)  # 模拟 I/O（网络/磁盘），此时 GIL 会释放
# 单线程：4 秒
start = time.time()
for _ in range(4): io_task()
print(f"Single: {time.time()-start:.2f}s")
# 双线程：≈1 秒
start = time.time()
t1 = threading.Thread(target=io_task)
t2 = threading.Thread(target=io_task)
t1.start(); t2.start(); t1.join(); t2.join()
print(f"Two threads: {time.time()-start:.2f}s")
```

Python中提供了一个multiprocessing模块,其创建的并非线程而是多进程,从而可以对CPU密集型任务实现并行执行,因为每个进程都独立有GIL.示例代码如下:

```python
import time
from multiprocessing import Process, Value
def cpu_bound(n, counter):
    """纯 CPU 密集型任务"""
    while n > 0:
        n -= 1
        counter.value += 1
if __name__ == '__main__':
    # 单进程测试
    counter1 = Value('i', 0)  # 共享整数
    start = time.time()
    cpu_bound(500000, counter1)
    print(f"Single process: {time.time() - start:.2f}s, count={counter1.value}")
    # 双进程测试（真正并行） 
    counter2 = Value('i', 0)
    counter3 = Value('i', 0)
    start = time.time()
    p1 = Process(target=cpu_bound, args=(250000, counter2))
    p2 = Process(target=cpu_bound, args=(250000, counter3))
    p1.start()
    p2.start()
    p1.join()
    p2.join() 
    total = counter2.value + counter3.value
    print(f"Two processes : {time.time() - start:.2f}s, count={total}")
```

单进程测试中纯CPU计算,没有涉及I/O等待,所以无线程切换,单核百分百占用.Value函数的作用是创建共享内存,虽然单进程的时候这个操作是冗余的,因为他不需要出现进程间的共享内存,所以其实也可以采用普通变量.其调用的语法结构:

```python
Value('i',0)
```

Value的第一个参数表示创建的内存变量类型,i表示整数,.d表示double类型,c表示char类型等.第二个参数则是设置的共享内存变量的初始值,访问/修改参数则用.value属性进行修改,

```python
counter.value+=1
```

本例中双进程使用两个独立Value,而非共享同一个.可以避免进程间的锁竞争,最大化并行效率.Process的语法结构和thread差不太多,不再赘述,但是他得到的是一个进程,而不是线程.程序执行流程是操作系统会创建两个独立进程,每个进程都有独立Python解释器和独立GIL,进程同时运行在不同的CPU核心上,无GIL争抢,计算真正的并行;join使得主进程阻塞等待子进程结束,即等到两个子进程计算完成.最后从两个共享内存中读取结果.这里用了main模块,是因为windows系统下没有fork()系统调用,需要重新导入主模块创建子进程,不然容易无限递归创建进程导致运行时间过长,Unix下可以省略.

在此我们解释一下进程和线程的区别.进程指的是操作系统分配资源的基本单位,拥有独立内存空间;线程则是CPU调度的基本单位,属于进程,共享进程内存.进程的内存空间是独立的不共享的,线程的空间则是共享所属进程的内存;进程的创建开销更大,因为它需要分配独立的解释器和GIL,复制相应内存,而线程的创建只需要分配调用栈,因此创建更快;进程的隔离性更好,因为单独的进程崩溃不会影响其他的进程,而线程的崩溃会导致整个所属进程挂掉,从而影响其余的进程;进程的安全性很高,因为他们的所属内存是天然隔离的,无需用锁,线程的安全性则并不高,因为共享内存需要手动同步,而且需要加锁对临界区加以保护;进程因为会分配独立的GIL,故而可以处理CPU的并行任务,而线程会因为需要竞争同一进程的GIL,导致CPU并发任务受限,更适合于I/O密集任务.

我们上面介绍了一些进程线程的知识,知道了一些并行操作的方式,但实际上程序运行中很容易出现异步操作的情况,也就是函数A需要调用函数B的结果,但是函数B此时还没有计算到这个结果,需要让函数等待.这里Python提供了Future类来保证异步操作的可行性.

```python
from concurrent.futures import Future
fut=Future()
# 等待结果
value=future.result()
# 设置结果(通常由另一个线程调用)
fut.set_result(value)
```

此时需要协调机制确保结果就绪后再调用.result().future是并发编程中的协调原语,代表异步操作的最终结果.result函数会阻塞当前线程,一直到结果被设置.常用于线程池,异步I/O等场景,是为了构建更高层的并发抽象的基础.

```python
import time, threading
from concurrent.futures import Future
def func(x, y, fut):
    time.sleep(20)
    fut.set_result(x + y)
def caller():
    fut = Future()
    threading.Thread(target=func, args=(2, 3, fut)).start()
    result = fut.result()  # 阻塞20秒
    print('Got:', result)
```

上例表示两个函数的并发执行,且这个模式会广泛应用于线程,异步,多进程等场景.主线程在start启动子线程后遇到result阻塞等待,子线程执行耗时操作后通过.set\_result通知主线程,主线程恢复执行并获取结果.


<a id="org2fc2fec"></a>

## Functional Programming

函数式编程风格是以函数为核心构建单元,不存在函数副作用,没有不可变数据,存在高阶函数(允许接受或返回函数的函数).函数式编程强调采用纯函数:相同的输入始终产生相同的输出,不修改外部状态;不可变性:避免修改原始数据,而是生成新数据;组合性:通过小函数组合构建复杂逻辑.Python虽然不是纯函数式编程语言,但是Python的高级特性是允许函数作为参数输入和输出,所以他其实也是支持函数式编程风格的.高阶函数的核心特征是函数可以接受其他函数作为参数,函数可以返回函数作为结果.我们以如下的两个相似函数为例,

```python
def sum_squares(nums):
    total=0
    for n in nums:
        total+=n*n
    return total
def sum_cubes(nums):
    total=0
    for n in nums:
        total+=n**3
    return total
```

上例中其实代码的基本结构是一样的,只有累加的函数不同.我们可以将相同的部分抽象成一个公共的函数体,通过输入函数来提供函数的差异部分,这样可以实现代码复用,提高代码可读性,回调函数是高阶函数的典型应用.

```python
def sum_func(nums,*,func=None):
    if func is None:
        raise Exception
    total=0
    for n in nums:
        total+=func(n)
    return total
```

单句表达式可以用lambda定义出函数,也就是lambda函数,可以创建匿名函数,即时创建即时定义.我们需要注意的是lambda函数仅能包含单一表达式,不支持控制流,异常等.lambda函数适合简单,一次性的函数场景,如键排序,映射转换等.复杂逻辑仍应该使用def定义具名函数从而可以提升代码可读性.不仅如此,lambda函数也可以用于固定函数参数,如

```python
def dis(x,y):
    return abs(x-y)
dis10=lambda x:dis(10,x)
```

但是这样代码可读性较差,Python的functools模块中提供了partial方法,可以将多参函数固定参数使得转换为少参函数,从而提升代码复用效率.

```python
from functools import partial
distance10=partial(dis,10)
print(distance10(2))
```

这里我们没有指定固定的参数位置,则默认为第一个参数.我们也可以直接指定固定某个函数参数如

```python
from functools import partial
def power(base, exponent):
    return base ** exponent
square = partial(power, exponent=2)
cube   = partial(power, exponent=3)
```

从上面计算平方和和立方和的代码中,我们可以意识到Python代码的一个重要机制,Map-Reduce模式.我们可以将计算拆解为两个步骤,第一个是Map过程,对每个元素都应用函数,其可以实现分布式并行计算;第二个则是Reduce过程,则是基于前一步的基础上,将结果以某种方式累积成一个值.我们将两个步骤显式拆开,如下所示:

```python
def map(func, values):
    return [func(x) for x in values]
def reduce(func, values, initial=0):
    result = initial
    for n in values:
        result = func(n, result)
    return result
nums = [1, 2, 3, 4]
result = reduce(lambda x, y: x + y, map(lambda x: x * x, nums))  # 30
print(result)
```

Python中存在内置函数map,其可以将函数直接作用在序列值.需要注意的是,map函数返回的实际上是一个迭代器,而不是列表,我们需要强制类型转换将结果变为列表.

```python
print(list(map(square, [1, 2, 3])))  
print(list(map(cube,   [1, 2, 3])))
```


<a id="org3c4bc7a"></a>

## Closures

闭包指的是如果内部函数作为结果被返回,那么这个内部函数就被称之为闭包,闭包会保留函数后续正常运行所需的所有变量的值.为了实现这一点,对外部变量(绑定变量)的引用会随函数一并携带.闭包通过closure属性保存对外部变量的引用.

```python
def add(x,y):
    def do_add():
        print(f'{x}+{y}->{x+y}')
    return do_add
a=add(3,4)
print(a)# <function add.<locals>.do_add>
print(a.__closure__) # (<cell: int object>, <cell: int object>)
print(a.__closure__[0].cell_contents) # 3
print(a.__closure__[1].cell_contents) # 4
a()
```

每个cell对象会封装一个被捕获的变量值,查看具体的存储结果需要调用cell\_contents来查看,并且closure属性是一个元组.

需要注意的是闭包只会捕获函数体内实际引用的变量,对于未使用的变量则不会被保留.

```python
def new_add(x,y):
    result=x+y
    def get_result():
        return result
    return get_result
b=new_add(3,4)
print(b.__closure__)
print(type(b.__closure__))
print(b.__closure__[0].cell_contents)
```

上面并不会保留x和y的值,而只会保留result的值,因为内部函数只需要使用result变量.闭包的变量是不允许随意修改的,但是我们如果期待闭包变量可变,那么就需要使用nonlocal声明变量,这样的话,闭包就可以持有可变的内部状态,功能类似对象或类.nonlocal允许内部函数修改外层作用域的变量,使闭包具有状态保持能力.

```python
def counter(n):
    def incr():
        nonlocal n
        n+=1
        return n
    return incr
c=counter(10)
print(c())
print(c())
```

闭包是Python的核心特征之一,常见应用包括:替代求值(延迟求值),回调函数,代码生成(宏).我们在此给出上述应用场景的相关代码实现.

```python
def delayed_computation(x,y):
    print('Prepared Done')
    def compute():
        print("Performing computation")
        return x+y
    return compute
result_func=delayed_computation(10,20)
print(result_func())
```

上面的代码是延迟求值的相关实现.延迟计算直到真正需要的时候才会执行.

```python
def make_callback(name,value):
    def callback():
        print(f'Callback {name}: value = {value}')
    return callback
cb1=make_callback('handler1',100)
cb2=make_callback('handler2',200)
cb1()
cb2()
def create_event_handler(event_name,handler_data):
    def handler(event):
        print(f"Event '{event_name}' triggered")
        print(f"Data: {handler_data}")
        print(f"Event details: {event}")
    return handler
click_handler=create_event_handler("click",{'count':0})
click_handler({'x':100,'y':200})
```

回调函数是因为闭包携带上下文信息,适合用作回调.

```python
def make_multiplier(factor):
    def multiplier(x):
        return x*factor
    return multiplier
double=make_multiplier(2)
triple=make_multiplier(3)
percent=make_multiplier(0.01)
print(double(10))
print(triple(10))
print(percent(10))
def make_formatter(prefix, suffix):
    """生成一个带前缀和后缀的格式化函数"""
    def formatter(text):
        return f"{prefix}{text}{suffix}"
    return formatter
bold = make_formatter("**", "**")
italic = make_formatter("*", "*")
quote = make_formatter("> ", "")
print(bold("Hello"))    # **Hello**
print(italic("World"))  # *World*
print(quote("Note"))    # > Note
```

闭包用于生成定制化的函数


<a id="org5e777d1"></a>

## Errors

异常捕获的语法块结构如下所示

```python
try:
    pass
except RuntimeError as e:
    pass
```

在函数中我们应该尽可能处理那些可以被恢复且具有恢复意义的异常.对于那些不好处理的异常,我们应该让他继续向函数外抛出异常,因为这类不好处理的异常通常表示更为复杂的问题.

```python
def read_csv(filename):
    f=open(filename)
    for row in csv.reader(f):
        try:
            name=row[0]
            shares=int(row[1])
            price=float(row[2])
        except ValueError as e:
            print('Bad row:',row)
            continue
```

上面我们只针对ValueError进行了处理,如果我们发现出现了FileNotFoundError,也就是文件不存在的异常,我们实际上在程序层面是没有合理的恢复手段,所以我们需要将其抛出交由程序运行者处理.对于异常处理而言,我们并不希望捕获所有的异常,除非是我们报告或记录了真正的异常信息,如

```python
try:
    pass
except Exception as e:
    print("Sorry, it didn't work.")
    print("Reason:",e)
```

如果我们不记录不报告真实异常,极易造成代码的无法维护.但是进一步,如果我们完全忽略代码异常的处理而强行推进程序,那么极易造成严重的程序事故.

在异常处理中,我们可能会希望记录抛出位置,或者对异常信息进行处理后重新抛出异常,我们可以在except语法块中重新调用raise从而抛出相同的异常.

```python
try:
    pass
except Exception as e:
    print("Sorry, it didn't work.")
    print("Reason:",e)
    raise
```

这样会将相同的异常再次向外抛出,需要强调的是,如果raise后面不接异常错误并且在except语法块之外,程序是会报错的.这样的操作适合于对异常进行处理后仍允许其向外传播.我们可以通过将异常包装成另一个异常的方式,来保留原始异常信息并且创建新的异常链.如下所示

```python
class TaskError(Exception):
    """自定义任务异常"""
    pass
def process_data(data):
    """底层处理函数"""
    if not data:
        raise ValueError("数据不能为空")
    return data.upper()
def run_task(data):
    """上层任务函数"""
    try:
        result = process_data(data)
        return result
    except Exception as e:
        # 保留原始异常信息，创建新的异常链
        raise TaskError('It failed') from e
try:
    run_task("")
except TaskError as e:
    print(f"捕获到: {e}")
    print(f"原始异常: {e.__cause__}")
```

例如上面的程序最初的异常是ValueError,在run\_task函数中我们将其包装为TaskError异常.但他依旧保留了原始异常信息,我们可以通过\_\_cause\_\_属性来调用他.这里的from就表示从原有的异常中继承包装抛出一个新的异常信息.这里异常处理中还存在一部分资源管理的问题,异常处理中仍然需要进行合理的资源管理,不然的话,就可能导致文件描述符泄漏,死锁或其他问题.比较经典的方法可以考虑finally语法块,其表示无论异常是否发生都会运行.

```python
try:
    pass
except Exception as e:
    pass
finally:
    pass
```

现代一点的方法则是使用with语法块来自动管理相关的资源.

```python
with open(filename) as f:
    try:
        pass
    except Exception as e:
        pass
```

应用程序应定义自己的异常,并且我们应该将Python内置异常保留给编程错误.应捕获而不是主动抛出异常.

在C/C++中,我们可以通过返回码的方式来设置函数的返回状态.但在Python中尽可能不要使用返回码,是因为返回码不是Python中表示错误得到标准方式,调用者常会遗忘检查,导致程序稍后因其他原因崩溃.使用logging模块记录诊断信息,

```python
import logging
log = logging.getLogger(__name__)

def read_data(filename):
    pass
    try:
        name = row[0]
        shares = int(row[1])
        price = float(row[2])
    except ValueError as e:
        log.warning("Bad row: %s", row)
        log.debug("Reason: %s", e)
```

这种记录方式通常会比print函数更合适.我们之前也已经介绍过logging模块,在此不再赘述.


<a id="org12da1f2"></a>

## Testing and Debugging

Python的动态特性提供了Python的很多方便的特性,但也使得代码测试对大多数应用至关重要,发现bug的唯一方法是运行并且确保覆盖其所有功能.断言是运行时检查,如果不符合断言则会报错,抛出AssertionError.

```python
def add(x, y):
    ''' Adds x and y '''
    assert isinstance(x, int)
    assert isinstance(y, int)
    return x + y
```

断言不应该用于检查用户输入而应用于验证程序不变量(如必须始终成立的内部条件).运行失败则表示编程错误,那么可以基于这个断言进行责任规划(如归咎于调用者).同样我们虽然写了断言,但是可能在运行中需要忽略断言的语句,所以我们可以禁用断言,用如下的调用Python解释器方式,

```shell
python -O Ch5_Ex5.py
```

Python的内置测试模块为unittest模块,其可以应用于标准库使用,广泛应用于其他项目.我们定义一个测试类,其必须继承自unittest.TestCase,并定义其中的测试方法,代码如下所示

```python
import simple
import unittest
class TestAdd(unittest.TestCase):
    def test_simple(self):
        # 用简单整数参数测试
        r = simple.add(2, 2)
        self.assertEqual(r, 5)
    def test_str(self):
        # 用字符串测试
        r = simple.add('hello', 'world')
        self.assertEqual(r, 'helloworld')
```

这里的每个测试方法必须要以test开头,这样的话才会被测试模块自动调用检测.我们稍微举例一下测试中的特殊断言,

```python
# 断言 expr 为 True
self.assertTrue(expr)
# 断言 x == y
self.assertEqual(x, y)
# 断言 x 与 y 近似相等
self.assertAlmostEqual(x, y, places)
# 断言会抛出异常
with self.assertRaises(SomeError):
    pass
```

如果我们需要运行unittest测试,那么应该添加以下的代码,

```python
if __name__ == '__main__':
    unittest.main()
```

unittest模块对于大型应用可能会变得十分复杂,并且unittest在测试运行,结果收集方面有大量选项.
