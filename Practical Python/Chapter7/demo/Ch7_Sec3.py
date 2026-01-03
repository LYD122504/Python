def add(x,y):
    def do_add():
        print(f"Adding {x} and {y}")
        return x + y
    return do_add
a=add(3,4)
print(a)
print(a())

def after(seconds,func):
    import time
    time.sleep(seconds)
    func()
def greet():
    print("Hello, world!")
after(1,greet)
def add(x, y):
    def do_add():
        print(f'Adding {x} + {y} -> {x+y}')
    return do_add

def after(seconds, func):
    import time
    time.sleep(seconds)
    func()

after(1, add(2, 3))
import builtins
print(dir(builtins))

total=0
def sum(arg1,arg2):
    total=arg1+arg2
    print('Local variable is ',total)
    return total
sum(10,20)
print('Global variable is ',total)

num = 1
def fun1():
    global num  # 需要使用 global 关键字声明
    print(num) 
    num = 123
    print(num)
fun1()
print(num)

def outer():
    num = 10
    def inner():
        nonlocal num   # nonlocal关键字声明
        num = 100
        print(num)
    inner()
    print(num)
outer()
a = add(3, 4)
print(a.__closure__)
print([c.cell_contents for c in a.__closure__])
# [3, 4]
def make_adder(n):
    def add(x):
        return x+n
    return add
add10 = make_adder(10)
add100 = make_adder(100)
print(add10(5))    # 15
print(add100(5))   # 105

funcs = []
for i in range(3):
    def f():
        return i
    funcs.append(f)
print([f() for f in funcs])

def make_counter():
    count=0
    def counter():
        nonlocal count
        count+=1
        return count
    return counter
c=make_counter()
print(c()) #1
print(c()) #2
print(c()) #3

def memorized_power():
    cache={}
    def power(base,exp):
        if (base,exp) in cache:
            print('Get from cache:')
            return cache[(base,exp)]
        print('Compute now')
        result=base**exp
        cache[(base,exp)]=result
        return result
    return power
f = memorized_power()
print(f(2, 10))  # 计算并缓存
print(f(2, 10))  # 从缓存中取出
print(f(3, 3))   # 计算并缓存