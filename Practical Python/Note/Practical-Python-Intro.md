---
title: Pratical Python for dabeaz-Introduction to Python
date: 2025-09-03 21:39:58
tags:
    - Computer Science
    - Python
categories: Python
---

本笔记完全基于David Beazley的Python教程-[Practical Python](https://dabeaz-course.github.io/practical-python/Notes/Contents.html).

## 1.1 A First Program

在交互模式下,Python提供了下划线变量\_,他会保存最后一个表达式的结果,例如:

```python
>>> 37*42
1554
>>> _*2
3108
>>> _+50
3158
```

但这只在交互模式下有用,我们并不会在程序中使用.

<!--more-->

在Python中,#用于引导单行的注释,多行注释则可以用三个单引号或双引号括起来的字符串来表示.

与C/C++不同,Python并不需要在使用每个变量前声明其类型,其命名规则与C/C++类似,不能以数字开头,不能使用Python的关键字(如if,while等),变量名区分大小写.变量会在首次赋值时创建,并且会根据赋值的值来决定变量的类型.因此,他和C/C++的类型最大的不同在于,他的变量类型其实是可以随着程序需要而改变的,例如:

```python
>>> height=442
>>> type(height)
<class 'int'>
>>> height=442.0
>>> type(height)
<class 'float'>
>>> height='Really tall'
>>> type(height)        
<class 'str'>
```

与C/C++不同,Python并不通过{}来表示代码块,而是通过代码的缩进来表示代码块,通常缩进4个空格,因此对于Python而言,代码的缩进并不是风格问题,而是语法的一部分.不同代码缩进表示不同的代码块,例如:

```python
while num_bills*bill_thickness<sears_height:
    print(day,num_bills,num_bills*bill_thickness)
    day=day+1 #ERROR
    num_bills=num_bills*2
```

这样的话day=day+1就会报错,因为他并不在while循环的代码块内.反之如果day=day+1并不做缩进,那么他就不在while循环内,而是while循环后的第一条语句,因此day=day+1只会执行一次.

Python的条件判断语句和C/C++类似,但是如果我们希望在if判断中检查多个条件,我们需要用elif来添加检查,而不是用else if:

```python
if a>b:
    print("a is greater than b")
elif a==b:
    print("a is equal to b")
else:
    print("a is less than b")
```

Python中并不需要引入其他的包文件,就可以用print函数打印输出,并且print函数可以接受多个参数,并且会在参数间自动添加空格:

```python
print("Hello","world!")
print("The answer is",42)
```

并且print函数会默认在输出的后面添加一个换行符,如果不希望添加换行符,可以在print函数中添加end参数:

```python
print("Hello","world!",end=' ')
print("The answer is",42)
```

Python中可以用input函数向用户打印提示并且以字符串的形式获取用户输入:

```python
name=input("What is your name? ")
print("Hello",name)
```

他比较适合于用于调试或者交互,而不适合于正式的程序输入.但这里与C/C++不同的是,Python的输入得到的只能是字符串类型,如果需要其他数据类型,需要用强制类型转换函数进行转换,例如:

```python
age = input('Enter your age\n:')
age=int(age)
age=age+1
print('Your age is', age)
```

因为他读取的是一行字符串,所以即使用户在输入的文本中输入了空格,他也会被当做字符串的一部分一起输入,并不会像C/C++那样,遇到空格就结束输入.然而,如果我们需要输入多个值,可以用split方法将字符串拆分为多个部分,例如:

```python
name,age=input('Enter your name and age:').split() #默认以空格拆分
name,age=input('Enter your name and age:').split(',') #以逗号拆分
```

如果我们得到的输入多个值是相同的类型,那么我们可以用map函数将拆分后的字符串转换为相同的类型,例如:

```python
a,b,c=map(int,input('Enter three integers:').split())
print(a,b,c)
# 如果我们并不知道输入的整数有多少个,可以用一个列表来接收
num_list=list(map(int,input('Enter some integers:').split()))
print(num_list)
```

值得注意的是,这个map函数他只针对于多个值都是相同类型的情况,如果多个值类型不同,那么就需要分别转换.

有时我们需要指定一个空代码块,用于if语句或者函数框架设计等,此时可以用pass关键字用来表示无操作语句.他并不会执行任何操作,只是一个占位符,可能用于后续代码的添加,例如:

```python
if a>b:
    pass
else:
    print("a is less than or equal to b")
```


<a id="orgecc21b8"></a>

## 1.2 Numbers

Python有三种数字类型:bool,int,float和complex.这里值得注意的是,Python中并没有对浮点数进行进一步分类,而是归为了一类float,因此python中并没有float和double之分.

bool类型可以与int和float类型进行混合运算,其结果类型仍与int和float相同,这相当于在运算过程中出现了隐式类型转换.在运算的过程中,True会被当做1,False会被当做0.

在int和float类型对应的运算中,其有与C/C++类似但结果不同的运算符:

```python
5/2 # 其结果为2.5,与C/C++的除法依赖于两侧操作数不同,python的/就是普通除法,无论两端操作数的类型,其结果都是float
5//2 #其结果为2,这其实相当于C/C++的整数除法,但是要求两端操作数均为整数时,其结果类型才为int
5.0//2 #其结果为2.0,两端操作数只要有一个为float时,其结果类型为float
3**2 #其结果为9,其就是C/C++的power函数,只不过power函数要求两个量均为double类型,而**则允许有整数
```

同样与C/C++一样,int也是有位运算的,并且float由于浮点数存储方式的差异并没有位运算.

与C/C++一样,Python也具有与或非三类逻辑运算符,但Python的运算符是and or not,并不是C中的&& || !.
