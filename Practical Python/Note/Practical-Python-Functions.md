---
title: Pratical Python-Functions and Error
date: 2025-10-21 19:50:33
tags:
    - Computer Science
    - Python
categories: Python
mathjax: true
---

本笔记完全基于David Beazley的Python教程-[Practical Python](https://dabeaz-course.github.io/practical-python/Notes/Contents.html).

## Functions and Script Writing

Python的编程风格更推荐于使用由下向上的代码编写风格. 我们将函数视作程序的构建块,从较小的,较简单的函数开始编写,后面的函数将在先前函数的基础之上继续编写.

在理想情况下,函数只对向函数输入的变量进行操作,避免对全局变量和未知的变量值变化带来的副作用.因此,构建函数的目的是模块化和可预测性.模块化是用来封装程序进程,从而利于程序编写和后期维护;可预测性,是为了避免函数造成一些未知的影响.

<!--more-->

函数中的类型注释,其代码如下所示,

```python
def func(var_name:var_type) -> return_type:
```

这些提示并不会影响函数的作用,只是起一个注释效果,并且即使实际的输入输出类型与注释的不符,IDE或者编译器可能会警告,但并不会影响程序的执行.


<a id="org35ec0fa"></a>

## More details on functions

可以在函数参数里面设置一些默认值,那么这些值就是可选参数,使用函数时可以不对其赋值,这样的话,函数会自动调用默认值,但是前提是这些可选参数必须在参数列表的末尾.

```python
def fun(var1,var2,var3=init1,var4=init4)
```

由于可选参数的存在,因此推荐参用关键字赋值的方式来传递函数参数,这样可以提高代码的清晰度和可读性.

```python
fun(item1,item2,var3=item3)
```

函数如果没有设置返回值或者return空,那么他的返回值为None.

```python
def fun():
    return
d=fun() # None
```

函数的返回值并不能同时分开的返回多个值,但可以通过元组的方式实现多值返回.

```python
def divide(a,b):
    q=a//b
    r=a%b
    return (q,r)
x=divide(11,3) # (3,2)
x,y=divide(11,3) # x=3,y=2
```

类似于C/C++的变量作用域的讨论,Python同样可以有这样的讨论;Python的外部变量是全局变量,在任意函数中都可以调用;而函数内定义的变量则是局部变量,其生存域仅在定义其的函数内部,出了函数就会被释放.函数虽然可以调用读取全局变量,但并不能在函数中随意修改全局变量的值.如果试图在函数内部修改外部的全局变量,可以用global关键字的方式来强行修改.全局声明要求其必须在使用前出现,并且相应的变量也必须和函数位于同一个文件中,因此这并不适合于多文件编程,并不推荐使用.

```python
name='David'
def fun():
    global name
    name='Guide'
    return name
test=fun()
```

值得注意的是,与C不同的是Python函数并不是传递变量值的副本,而是传递变量引用的副本,因此对于可变类型的参数可以直接在函数内修改,至于不可变类型需要利用局部变量的方式来重新赋值修改.

```python
def fun(a):
    a.append(1)
```

事实上,如果修改值和重新分配变量名称是存在一些差异的;修改值可以直接利用自带方法就地修改,而如果重新通过设置同名局部变量赋值的方式,他并不会影响外层全局变量.

```python
def bar(items):
    items=[4,5,6]
b=[1,2,3]
bar(b)
print(b) # [1,2,3]
```


<a id="org756e1b4"></a>

## Error Checking

Python不对函数参数类型或值执行类型检查或类型验证.函数将处理与函数语句兼容的数据类型.

```python
def add(a,b):
    return a+b
add(3,4) # 7
add('Hello',' World') # 'Hello World'
add('3','4') # '34'
```

异常用于在程序发生错误的时候将错误信息发送给程序.除了程序本身运行中可能导致异常信息出现,也可以利用raise方式来手动引发异常.

```python
def fun(a,b):
    if isinstance(a,str):
        raise RuntimeError(f'{a} is not right type'}
```

类似于C/C++,Python也可以通过try-except代码块来捕获程序抛出的异常,值得注意的是,异常的传播并不是从内层一直传播到外层的,而是如果出现第一个匹配的except,异常的传播就会停止,并不会继续向外传播.

```python
def foo():
    raise RuntimeError('Test')
def bar():
    try:
        foo()
    except RuntimeError as e:
        pass
def spark():
    try:
        bar()
    except RuntimeError as e:
        pass
    # 如果调用spark函数,那么他的异常其实是会被bar里面的except捕获后,终止程序
```

我们可以发现这个except捕获异常的时候同时还赋值了变量e,其实这是捕获异常的同时,将异常实例对象赋值给了变量e,但是我们如果将e打印出来,其实和字符串的表示类似.因此我们把try-except语法块的通用形式给出,

```python
try:
    statements
except Error as e: # 捕获异常信息
    statements # 处理异常信息的语句
    statements # 完成异常捕捉和处理后继续执行语句
```

如果一个函数或一个语句块中可能抛出多种异常,显然我们可以不断堆叠except代码块的方式来捕获多种异常.

```python
try:
    statement
except LookupError as e:
    statement
except RuntimeError as e:
    statement
except IOError as e:
    statement
except KeyboardInterrupt as e:
    statement
```

但是这样的话会将代码的长度毫无意义的增长,因此可以将相同处理方式的异常写成更为紧凑的形式.

```python
try:
    statement
except (IOError,LookupError,RuntimeError) as e:
    statement
```

这里利用e来存储抛出的异常实例,如果不用e来存储相应异常实例,容易导致虽然出现异常,但并不能显示得出异常的原因.而且这样的异常元组的方式只能应用于对异常的相同处理,如果对不同的异常有不同的处理方式,则不可以使用这类方法.

如果并不确定程序运行中会出现什么类型的异常,是可以通过使用Exception的方式来捕获全部的异常,但这并不适合于程序中大规模使用,因为他虽然能够捕捉所有的异常但并不知道错误原因,因此不利于程序的后期修改.

```python
try:
    statement
except Exception as e: # 虽然他可以捕捉所有的异常信息,但通过赋值e使得异常信息被存储下来,从而有利于后期检查
```

但对于异常捕捉建议遵从以窄捕捉为主,只捕捉自己能够处理的,对于不能处理让外层处理或尝试避免.

由于异常只会被第一次匹配的except捕捉,而不会继续向外传播,我们可以通过raise函数继续引发异常,让外层except继续捕捉异常.

```python
def bar():
    try:
        foo()
    except RuntimeError as e:
        raise
```

这里raise后并没有接参数,实际上就是直接将已经实例化的变量e向外层抛出,继续由外层except捕捉.

对于某些重要资源管理(如文件,线程池,CPU资源占用等可能出现死锁现象的资源),即使抛出异常需要仍然利用某些关闭措施,来结束资源占用.故而finally代码块会要求程序无论是否出现异常,无论异常的类型都需要在最后一步执行.

```python
try:
    fun()
except Exception as e:
    pass
finally:
    ending statement # 释放系统内部空间
```

