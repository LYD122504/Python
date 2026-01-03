---
title: Practical Python-Closure
date: 2026-01-03 09:31:31
tags:
    - Python
categories: Practical Python
mathjax: true
---

本笔记完全基于David Beazley的Python教程-[Practical Python](https://dabeaz-course.github.io/practical-python/Notes/Contents.html).

## Returning function and closures

在Python中,函数和整数,字符串一样都是对象.因此函数可以作为另一个函数的返回值,函数可以赋值给变量,函数可以作为参数传递.如

```python
def add(x,y):
    def do_add():
        print('Adding',x,y)
        return x+y
    return do_add
a=add(3,4)
```

这里的add函数并没有执行加法,而是返回了一个执行加法的新函数do\_add.这里的变量a指向的是函数do\_add,因此可以用a()的方式来调用内部函数.

<!--more-->

上面中我们发现do\_add函数可以调用函数体以外的变量,这是内部函数引用由外部函数定义的变量.在此我们需要介绍一下python的变量作用域.Python读取一个变量名,会按照如下顺序查找:L(Local)-E(Enclosing)-G(Global)-B(Built-in).这些分别表示如下作用域

1.  L(Local):最内层,包含局部变量,如一个函数/方法的内部

2.  E(Enclosing): 包含非局部也非全局的变量,例如两个嵌套函数,一个函数A中包含了一个函数B,那么对于B来说A的内部变量就是Enclosing作用域.

3.  G(Global):当前脚本的最外层,比如当前模块的全局变量

4.  B(Built-in):包含了内建的变量/关键字等,最后被搜索

    ![2026-01-01_23-51-50_screenshot](https://github.com/LYD122504/picx-images-hosting/raw/master/20260103/2026-01-01_23-51-50_screenshot.1e931o03gn.png)

```python
g_count=0 #Global
def outer():
    o_count=1 #Enclosing
    def inner():
        i_count=2 #Local
```

最后的内建变量/关键字是通过一个名为builtin的标准模块来实现,我们可以用如下代码来查看预定义的变量,

```python
import builtins
dir(builtins)
```

Python中只有模块(module),类(class)以及函数(def,lambda)才可以引入新的作用域,其他的代码如if/elif/else,try/except,for/while是不会引入新的作用域,也就是这些语句定义的变量,代码块外也是可以访问的.

```python
if True:
    x=1
print(x) #1
def test():
    y=10
    return y
print(y) #error
```

定义在函数内部的变量拥有一个局部作用域,定义在函数外的拥有全局作用域.局部变量只能在其被声明的函数内部访问,全局变量可以在整个程序范围内访问.在函数内部声明的变量只在函数内部的作用域中有效，调用函数时，这些内部变量会被加入到函数内部的作用域中，并且不会影响到函数外部的同名变量.

```python
total=0
def sum(arg1,arg2):
    total=arg1+arg2
    print('Local variable is ',total)
    return total
sum(10,20)
print('Global variable is ',total)
```

从此我们可看出,虽然全局变量可以在整个文件都可以被访问,但如果函数内部定义了同名的局部变量,那么就会把他给覆盖掉.

上面我们提到了同名的局部变量会把全局变量给覆盖掉,如果我们真的想要修改全局变量,那么可以使用global关键字,但是在使用global关键字之前一定要保证这个变量出现并存在过.

```python
num = 1
def fun1():
    global num  # 需要使用 global 关键字声明
    print(num) 
    num = 123
    print(num)
fun1()
print(num)
```

同样如果想要修改嵌套作用域(enclosing作用域)的变量,那么就需要使用nonlocal关键字,如下所示

```python
def outer():
    num = 10
    def inner():
        nonlocal num   # nonlocal关键字声明
        num = 100
        print(num)
    inner()
    print(num)
outer()
```

当一个内部函数引用了外部函数的局部变量，并且该内部函数在外部函数返回后仍然存在，这个内部函数就称为闭包.所以闭包可以认为就是一个函数被封装在一个局部变量环境中.这样可以延长局部变量的生存时间,如上面的add函数,当add函数执行结束,理论上局部变量应该被释放掉,但是由于do\_add还需要使用这些变量,因此Python仍然会保留这些变量在闭包环境中.我们可以用如下方式来查看局部变量在闭包中的生存方式,

```python
a = add(3, 4)
print(a.__closure__)
#(<cell at 0x...: int object at ...>,
#<cell at 0x...: int object at ...>)
print([c.cell_contents for c in a.__closure__])
# [3, 4]
```

这里的局部变量并不是直接复制到函数参数里面,而是通过存放在闭包单元中等待访问,do\_add通过cell来间接访问它们.闭包的关键特性为闭包保留了函数正常运行所需的所有变量的值.可以将闭包视为一个函数加上一个额外的环境,该环境保存它所依赖的变量的值.

闭包的经典用途一:延迟求值,其代码如下:

```python
def after(seconds, func):
    import time
    time.sleep(seconds)
    func()
def greeting():
    print('Hello Guido')
after(30, greeting)
after(30,add(2,3))
```

他的执行逻辑是先执行add函数,将参数绑定到闭包单元并且返回闭包do\_add,30s后after再执行do\_add函数.所以其实是先绑定函数参数到闭包单元,然后再执行闭包函数逻辑.

闭包的经典用途二:避免代码重复.闭包本质上是生成函数的函数.

```python
def make_adder(n):
    def add(x):
        return x+n
    return add
add10 = make_adder(10)
add100 = make_adder(100)
print(add10(5))    # 15
print(add100(5))   # 105
```

他的优势在于不需要写多个基本上一样的函数,参数n成为函数的内置配置.

对于闭包有一个十分细节的问题是晚绑定(Late Binding),代码如下

```python
funcs = []
for i in range(3):
    def f():
        return i
    funcs.append(f)
print([f() for f in funcs])
# [2, 2, 2]
```

因为闭包捕获的是变量i的值,而不是i当时的值.因为其实这里的i并没有立刻求值,而是后续调用的时候才会去找i,这个时候循环已经结束了,所以i已经是2了.如果我们要调用i的当前值可以做如下改动

```python
funcs = []
for i in range(3):
    def f(i=i):
        return i
    funcs.append(f)
print([f() for f in funcs])
```

我们给几个闭包比较经典的示例:计数器,缓存计算和模拟私有变量.

```python
#计数器
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
```

这里的count定义在make\_counter函数中,counter闭包会调用count这个变量,并利用nonlocal关键字修改enclosing环境变量.每调用一次c(),count都会自增一次.

```python
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
f = memoized_power()
print(f(2, 10))  # 计算并缓存
print(f(2, 10))  # 从缓存中取出
print(f(3, 3))   # 计算并缓存
```

这里利用闭包来维护一个私有的cache字典,只有通过闭包函数来访问cache字典.

```python
def make_account(initial_balance):
    balance = initial_balance
    def deposit(amount):
        nonlocal balance
        balance += amount
        return balance
    def withdraw(amount):
        nonlocal balance
        if amount > balance:
            return "余额不足"
        balance -= amount
        return balance
    def get_balance():
        return balance
    return deposit, withdraw, get_balance
deposit, withdraw, get_balance = make_account(100)
print(deposit(50))      # 150
print(withdraw(30))     # 120
print(get_balance())    # 120
print(withdraw(200))    # 余额不足
```

这里的balance作为enclosing环境变量的方式存储,他被完全封装在闭包函数里面,因此通过闭包函数返回的函数来操作其值.
