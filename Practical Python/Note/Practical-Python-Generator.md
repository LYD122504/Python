---
title: Practical Python-Iterator and Generator
date: 2025-12-25 23:06:09
tags:
    - Python
categories: Practical Python
mathjax: true
---

本笔记完全基于David Beazley的Python教程-[Practical Python](https://dabeaz-course.github.io/practical-python/Notes/Contents.html).

## Iteration protocol

在前面的讨论中,我们多次使用了容器迭代的程序,但是我们并没有深入了解过的迭代循环的底层实现,因此我们在此先介绍他的底层实现.

```python
_iter=obj.__iter__()
while True:
    try:
        x=_iter.__next__()
        # statements
    except StopIteration:
        break
```

这里的obj表示一个可迭代对象,而\_iter则表示迭代器对象.根据上面的底层实现来看,循环迭代的行为是基于迭代器对象.

<!--more-->

迭代器在Python中并非一个模糊的概念,而是具有严格技术定义的对象类型.一个对象只要同时具备\_\_iter\_\_()和\_\_next\_\_()方法,并遵守停止约定,那么就是一个合法的迭代器.对于\_\_iter\_\_()方法而言,他会返回一个迭代器对象,一般来说都是他自己,如果不是他自己,那么其实并不是传统意义上的迭代器,但本质上没有影响.

```python
def __iter__(self):
    return self
```

for会先调用iter(obj),iter(obj)则会在内部查找obj.\_\_iter\_\_().

\_\_next\_\_()返回下一个元素或迭代终止.

```python
def __next__(self):
    if EndCondition:
        raise StopIteration
    return NextValue
```

其每被调用一次,都会推进一次内部状态;到迭代终止状态时,那么结束时必须抛出异常StopIteration;不能返回特殊值表示结束.

迭代器是存在一个读取状态的.

```python
it=iter([1,2,3])
next(it) #1
next(it) #2
next(it) #3
next(it) #StopIteration
```

状态是会随着next读取不断前进,但是不能自动回退的.

迭代器一般来说是一次性的.

```python
it = iter([1,2,3])
list(it)  # [1,2,3]
list(it)  # []
```

这其实就是iterator和iterable的关键区别


<a id="org9628608"></a>

## Customizing Iteration with Generators

生成器generator指的是一个定义迭代的函数.

```python
def countdown(n):
    while n>0:
        yield n
        n-=1
```

从上面的代码中,我们意识到生成器其实是任意使用yield语句的函数.与普通的函数不同,调用生成器函数会创建一个生成器对象,但并不会立刻执行函数.

```python
x=countdown(10)
print(x) # <generator object countdown at 0x0000020956043850>
```

函数只在\_\_next\_\_()方法调用下不断推进函数内部状态.yield产生一个值之后,会挂起函数执行,直到函数下一次调用\_\_next\_\_()方法恢复执行;同样在函数迭代的结束时会引发一个异常.

进一步介绍一些Generator的概念.Generator是一种惰性求值的迭代器,用于按需产生序列中的元素,并不是一次性的把所有结果存入内存,换言之,生成器其实是一个带状态的可暂停执行的函数,每次恢复时都从上次yield的位置继续执行.

生成器本身就是一个迭代器,他满足我们之前提及的迭代器协议,即\_\_iter\_\_()函数返回生成器本身做迭代器;\_\_next\_\_()函数返回下一个值或者抛出StopIteration异常.

```python
gen = (x*x for x in range(3))
iter(gen) is gen        # True
next(gen)               # 调用 __next__()
```

这里我们用到了一个类似于列表表达式的东西,他其实是生成器表达式,他返回的会是一个生成器对象,我们会在后续的笔记中介绍这一用法,在此不再赘述.

我们开始介绍Generator的运行流程.首次调用next()方法,会先从函数的第一行开始执行,一直遇到yield value的语句,他会返回value,然后就是生成器的十分重要的性质了,他会冻结当前执行现场(包括栈帧,局部变量和指令指针等);后续调用next()方法,会从上次yield的下一行开始执行,直到再次遇到yield返回新值;若函数结束,则会抛出StopIteration.

```python
def demo():
    x=1
    yield x
    x+=1
    yield x
# 执行流程 next->yield 1(x=1被保存)
# 执行流程 next->yield 2(x=2被保存)
# 执行流程 next->StopIteration
```

yield的语义表示他会产生一个值并暂停函数执行,保存当前的执行状态.这使得Generator本质上是一个可恢复执行的协程原型.

协程原型通常指一种尚未具备完整并发调度机制但已经体现协程核心语义的语言结构.换言之,他可以实现暂停和恢复执行的能力,但是他的调度并不是通过系统完成的,而是需要用户或者库函数显式控制.协程的本质能力有三点:可挂起,可恢复以及保持执行状态,而Generator已经具备了这三个能力,因此理论上生成器已经是一个完整的协程交互模型.但是其与真正的协程还差一个调度器来实现他的自动调度.

这里我们就开始基于这个生成器,我们逐步解释python中的协程原型的实现.从生成器开始,代码如下:

```python
def gen():
    print("start")
    yield 1
    print("resume")
    yield 2
    print("stop")
g=gen()
print(next(g))
print(next(g))
```

这里函数可以被暂停,执行状态(局部变量和指令指针)被保存,再次调用next()时从原地恢复;但他还不是协程,他不能实现向函数的传值以及只能单向涉及从yield向外部传值.

利用send()函数给生成器提供了双向传值的能力,使得生成器具有一定协程原型的能力.

```python
def gen():
    print("coroutine started")
    x = yield          # 接收外部 send 的值
    print("got:", x)
    y = yield x + 1
    print("got again:", y)
g=gen()
next(c) #启动协程
print(c.send(10))
```

这一过程中我们将yield返回的值改成了一个表达式,并且提供了值双向传播的方式:外部到协程是send函数,协程到外部是yield语句.这里的send函数会传入值之后继续向后执行,类似于赋值后执行next函数.但这里我们距离真正的协程还差几个问题,没有调度器,没有并发,需要用户手动send/next.

利用协程调用协程,给出一个可组合协程的demo.

```python
def sub():
    x=yield
    yield x*2
    return "done"
def main():
    result=yield from sub()
    print("sub returned:",result)
m=main()
next(m)
print(m.send(10))
```

这里的第一个next在main()函数中会运行到yield from语句,并进入sub函数在x=yield语句停止;紧接着,send(10),会给x赋上10,并返回20且冻结函数状态.如果我们再用一个next,首先他会执行return done,并且在main中打印结果同时抛出终止迭代的异常.这里其实我们实现了协程的自动转发,具有了函数调用级组合性.

现代的协程原型代码如下所示:

```python
import asyncio
async def coro(name):
    print(name, "start")
    await asyncio.sleep(1)
    print(name, "end")
async def main():
    await asyncio.gather(
        coro("A"),
        coro("B")
    )
asyncio.run(main())
```

我们逐行解释上述代码,async def定义的是原生协程函数,调用他的时候并不会执行函数体,而是生成一个coroutine object,这个和我们前面介绍的Generator一样只是前者生成的是可迭代对象,而async def生成的则是可await对象.但值得注意的是coroutine object只能await一次,如果希望多次await需要进一步做封装成Task,不在此介绍.

coro函数体的第一个print函数并不会在coro("A")的时候调用,而是会在事件循环调度开始的时候才执行.asyncio.sleep(1)返回一个awaitable对象,这个对象会注册一个1s后的回调,并且将当前协程挂起,把控制权交还给事件循环.await的简单理解像是工作停止后告诉事件循环先去处理其他的任务,1s后再回来运行.下一个print则是在sleep(1)完成后,事件循环在1s后重新调度该协程的时候继续执行.

原生协程函数main()中的asyncio.gather()函数的作用,其中的coro()函数用于创建两个协程对象但并不会执行协程对象.asyncio.gather则是用于接受多个awaitable对象,并且把他们注册到事件循环,并发调度,并且返回一个新的awaitable对象.这里是用的并发调度而不是并行调度,因此本质上还是单线程协作式并发.

最后的asyncio.run(main())则是创建了事件循环,执行main()协程,并且关闭事件循环清理资源.

| 语句           | 作用         |
| -------------- | ------------ |
| async def      | 定义协程     |
| await          | 让出控制权   |
| asyncio.gather | 管理并发     |
| asyncio.run    | 驱动事件循环 |
