---
title: Practical Python-Coroutine
date: 2025-12-28 16:39:36
tags:
    - Python
categories: Practical Python
mathjax: true
---

## Coroutine

协程函数是使用async def定义的函数.

```python
async def f():
    pass
```

其在调用不会执行函数体,仅返回一个coroutine object,只创建了一个可等待对象(awaitable).协程对象是协程函数的返回值,本质上是一种可等待对象,他的内部保存函数体,局部变量,当前执行位置(尚未开始/挂起点).他的调度状态一般为CREATED/RUNNING/SUSPENDED/FINISHED,用于调度分析.

<!--more-->

Awaitable表示可等待对象,表示任意可以被await挂起的对象:coroutine object;Task;Future.await X的行为取决于X是否已经完成.await表示协程挂起点/调度点,这是协程调度中唯一的合法的协程挂起点.await X的不同行为:X结束则立刻结束,X不结束则挂起当前协程,把控制权交还给事件循环.await则是协程调度的关键. Event loop是一个持续运行的调度器,负责管理任务,调度协程执行,在协程挂起/恢复切换.他是单线程协程式调度系统,他并不是抢占式调度系统,因为asyncio只在await处挂起,并不会打断协程的运行.

```python
import asyncio
#get_event_loop是在函数中读取事件循环的,如果没有则新建并绑定事件循环
loop=asyncio.get_event_loop()
#new_event_loop是新建事件循环,set_event_loop绑定事件循环
loop=asyncio.new_event_loop()
asyncio.set_event_loop(loop)
```

任务是被事件循环管理的协程包装器,

```python
task=asyncio.create_task(coro)
```

他的作用是coroutine object注册到事件循环,让事件循环意识到协程的存在.事件循环只调度任务,不直接调度协程对象.Ready表示一个task当前可以继续执行,这些任务一般由未完成或不在sleep,不在I/O阻塞中的.准备队列则是事件循环内部会维护一个可运行的任务队列,如果协程运行到某个await语句时,挂起后从其中挑选一个任务执行.suspended状态表示协程执行到await时,任务被挂起,等待某个未完成对象的状态.

```python
await asyncio.sleep(1)
await some_future
```

他会将当前任务从准备队列中移除当前任务,待条件满足后重新写入准备队列.对于协程调度来说,事件循环会在准备队列中选取一个准备任务将其推进执行,不抢占资源,但不保证公平分配,也不一定按照先进先出的顺序.asyncio.gather()函数则是接受多个awaitable对象,并将这些注册成任务,将其并发完成.并发并不是并行,他们仍是单线程的.

简单的调度流程:当多个Task被创建,事件循环依次推进任务,直到遇到第一个await语句.当协程遇到await处主动暂停,并将这个任务挂起,把控制权交还事件循环.我们开始逐步加深调度流程的复杂度.

```python
async def f():
    print("A")
    print("B")
    print("C")
asyncio.run(f())
#A B C
```

这个程序中没有await挂起任务,因此代码不可以被打断,事件循环无法介入.这里用了asyncio.run()函数接受协程,只能一次性使用,并在最后会将创建的事件循环清理关闭.

单协程并只有一个await语句,其运行顺序仍然确定.

```python
async def f():
    print("A")
    await asyncio.sleep(1)
    print("B")
asyncio.run(f())
#A (wait 1s) B
```

上面的程序中除了协程函数f外,没有其他的任务.因此await就算挂起,也无法在准备队列中找到另一个任务运行,故而他需要暂停1s后再打印B.

顺序await必然串行

```python
async def f():
    print("f start")
    await asyncio.sleep(1)
    print("f end")
async def g():
    print("g start")
    await asyncio.sleep(1)
    print("g end")
async def main():
    await f()
    await g()
asyncio.run(main())
# f start (1s) f end
# g start (1s) g end
```

main函数中的两个await是一个串行逻辑,f还没有结束,g根本还不会运行,以协程的方式进入事件循环,因此他的结果会是一个顺序输出.

使用gather()函数并发执行

```python
async def f():
    print("f start")
    await asyncio.sleep(1)
    print("f end")
async def g():
    print("g start")
    await asyncio.sleep(1)
    print("g end")
async def main():
    await asyncio.gather(f(), g())
asyncio.run(main())
# fstart gstart fend gend
```

gather会同时注册多个任务,一般来说是从左到右推进,依次将其推进到第一个await,触发第一个await才会进入真正的协程调度阶段.

create\_task函数在无await语句的情况下

```python
async def child():
    print("child start")
async def main():
    print("main start")
    asyncio.create_task(child())
    print("main end")
asyncio.run(main())
# mainstart mainend childstart
```

main函数在输出start后将child()协程转换为任务后由于没有遇到挂起,因此会继续执行main,并将child放入准备队列;等main()协程运行结束,才会运行child任务.

create\_task()函数加上await语句,

```python
async def child(name):
    print(name, "child start")
    await asyncio.sleep(0)
    print(name, "child end")
async def parent(name):
    print(name, "parent start")
    asyncio.create_task(child(name))
    await asyncio.sleep(0)
    print(name, "parent end")
async def main():
    A=asyncio.create_task(parent("A"))
    B=asyncio.create_task(parent("B"))
    await asyncio.gather(A,B)
asyncio.run(main())
# Astart Bstart Achildstart Aend Bchildstart
# Bend Achildend Bchildend
```

他的调用本质上其实是一个队列的先进先出原则,因此所以我们只需要在推演过程中记录所谓的准备队列即可.值得注意的是,如果我们这里不在main函数里面加上await,那么run只会运行完main协程直接释放掉整个事件调度,可能多跑一下A,B到第一个await.这是因为我们的run是基于main构建的,而main中没有await将其挂起,那么只会将其执行完后释放资源.因此执行顺序其实基于同一任务内的确定顺序以及await导致的不确定性运行.
