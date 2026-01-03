import asyncio
async def f():
    pass


async def f():
    print("A")
    print("B")
    print("C")
asyncio.run(f())

async def f():
    print("A")
    await asyncio.sleep(1)
    print("B")
asyncio.run(f())

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

async def child():
    print("child start")
async def main():
    print("main start")
    asyncio.create_task(child())
    print("main end")
asyncio.run(main())

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