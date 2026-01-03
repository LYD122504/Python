def countdown(n):
    while n>0:
        yield n
        n-=1
for x in countdown(10):
    print(x,end=' ')
def countdown(n):
    # Added a print statement
    print('Counting down from',n)
    while n>0:
        yield n
        n-=1
x=countdown(10)
print(x)
print(x.__next__())
print(x.__next__())

gen = (x*x for x in range(3))

print(gen)
print(iter(gen) is gen)        # True
print(next(gen))               # 调用 __next__()

def gen():
    print("start")
    yield 1
    print("resume")
    yield 2
    print("stop")
g=gen()
print(next(g))
print(next(g))

def gen():
    print("coroutine started")
    x = yield          # 接收外部 send 的值
    print("got:", x)
    y = yield x + 1
    print("got again:", y)
c=gen()
next(c) #启动协程
print(c.send(10))
#print(next(c))

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

import asyncio

async def worker(name, delay):
    print(f"{name}: start")
    await asyncio.sleep(delay)
    print(f"{name}: after sleep {delay}")
    await asyncio.sleep(0)
    print(f"{name}: end")
    return name

async def group():
    print("group: start")

    a = asyncio.create_task(worker("A", 1))
    b = asyncio.create_task(worker("B", 0))

    print("group: tasks created")

    r1 = await a
    print("group: got", r1)

    r2 = await b
    print("group: got", r2)

    print("group: end")

async def main():
    print("main: start")

    await asyncio.gather(
        group(),
        worker("C", 0.5)
    )

    print("main: end")

asyncio.run(main())

import asyncio

async def sub(name):
    print(f"{name}: sub start")
    await asyncio.sleep(0)
    print(f"{name}: sub end")
    return name

async def worker(name):
    print(f"{name}: start")

    t = asyncio.create_task(sub(name))
    print(f"{name}: task created")

    await asyncio.sleep(0)
    print(f"{name}: after sleep")

    r = await t
    print(f"{name}: got {r}")

    print(f"{name}: end")

async def main():
    print("main: start")

    await asyncio.gather(
        worker("A"),
        worker("B"),
    )

    print("main: end")

asyncio.run(main())

async def ping(name):
    print(name, "start")
    await asyncio.sleep(0)
    print(name, "end")

async def main():
    for i in range(5):
        asyncio.create_task(ping(f"T{i}"))
    await asyncio.sleep(0)

asyncio.run(main())

import asyncio

async def child(name):
    print(f"{name}: child start")
    await asyncio.sleep(0)
    print(f"{name}: child end")

async def parent(name):
    print(f"{name}: parent start")

    t = asyncio.create_task(child(name))
    print(f"{name}: child task created")

    await asyncio.sleep(0)
    print(f"{name}: parent after sleep")

    await t
    print(f"{name}: parent end")

async def main():
    print("main start")

    await asyncio.gather(
        parent("A"),
        parent("B"),
    )

    print("main end")

asyncio.run(main())

import asyncio

async def worker(name):
    print(f"{name}: worker start")
    await asyncio.sleep(0)
    print(f"{name}: worker end")

async def task(name):
    print(f"{name}: task start")

    t = asyncio.create_task(worker(name))
    print(f"{name}: worker task created")

    await asyncio.sleep(0)
    print(f"{name}: task after sleep")

    await t
    print(f"{name}: task end")

async def main():
    print("main start")

    tA = asyncio.create_task(task("A"))
    await asyncio.sleep(0)              # ★ 关键变化点
    tB = asyncio.create_task(task("B"))

    await asyncio.gather(tA, tB)

    print("main end")

asyncio.run(main())
