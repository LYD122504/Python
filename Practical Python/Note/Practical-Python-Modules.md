---
title: Pratical Python-Modules
date: 2025-12-12 15:58:08
tags:
    - Computer Science
    - Python
categories: Python
mathjax: true
---

本笔记完全基于David Beazley的Python教程-[Practical Python](https://dabeaz-course.github.io/practical-python/Notes/Contents.html).

## Modules

模块可以认为是命名值的集合,换言之,模块其实和C++中的命名空间十分类似.模块中包含模块文件中定义的全局变量和定义的函数.当我们导入模块之后,如果需要调用模块中的命名值,只需要将模块名作为前缀调用即可. 在不同的模块中,是允许存在有相同名称的全局变量或函数的,对其调用如下所示

<!--more-->

```python
# foo.py
x=1
def foo:
    pass
# bar.py
x=1
def bar:
    pass
# main.py
import foo
import bar
print(foo.x)
print(bar.x)
```

因此,从上面的示例代码中,我们可以发现模块其实是互相独立的,所以模块其实可以做一些代码的命名上的隔离.但是上面我们导入模块的方式是利用import,如果我们采用下面的方式导入x,那他的隔离特性就会被我们破坏:

```python
from foo import x
from bar import x
```

如果是这样的话,x只会是bar模块中的值,并不会出现前面的隔离情况.

在程序导入模块的时候,模块的源文件会被完整执行到文件末尾.因此,如果源文件中存在某些全局范围下可执行的语句,在导入模块的同时这些语句会被执行.模块的命名空间中存储的是模块源文件中定义的全局变量以及函数文件.但是这里我们需要明确的一点是,这里存储的全局变量指的是在文件末尾的依然存在的全局变量,对于代码中间释放的全局变量则不会存储.

导入模块的方式如下所示

```python
import modules # 导入模块
import modules as nickname # 导入模块并重命名
from modules import func # 导入模块中的特定函数
```

这里有一些注意的点:模块只会在程序中导入一次,重复import相同的模块并不会重复执行模块的源代码,重复导入只会返回对之前加载模块的引用.因此,在jupyter或交互模式中,如果我们先导入了模块,再修改模块的代码,程序并不会做重复导入,我们需要重启解释器内核.

Python中用sys.module来存储已经加载模块的字典,sys.path则是用来存储Python查找模块时的参考路径列表,值得注意的是当前工作目录总是最优先的.

```python
import sys
print(sys.modules.keys()) # 存储已经加载模块的键值
print(sys.path) # 存储Python查找模块时的参考路径列表
```

这里的查找参考路径可能没有包含希望的模块,因为sys.path是一个列表,所以我们可以用append的方式把期待的路径添加进去.当然也可以通过环境变量的方式添加到搜索路径.

```python
import sys
sys.path.append('/project/foo/pyfiles')
```

但一般来说并不推荐自己手动修改搜索路径,除非某些异常需要手动导入路径.


<a id="org741ec56"></a>

## Main Module

Python和C/C++不同,他没有主函数或方法;但是Python具有主模块,主模块则是第一个运行的源文件.因此可以认为提供给Python解释器的文件就是主模块,在这个主模块文件调用的其他的模块则不是main模块.这里为了验证文件的调用形式,可以\_\_name\_\_来判断:

```python
if __name__=='__main__':
    statements
```

上面的代码表示如果文件以主模块文件的形式那他可以运行if条件的语句.如果不是以主模块文件的形式运行,那他的\_\_name\_\_变量为模块名.

任意的源文件都可以以主模块或者库模块的形式运行或导入调用.模块的常用结构如下所示:

```python
import module
variable
def func():
    pass
def foo(x):
    pass
if __name__=='__main__':
    statements
```

python不止可以利用IDE运行,也可以用命令行中调用解释器,所以和C/C++一样,python可以使用命令行参数,如下所示

```shell
python source.py
python source.py data1.csv
```

python的命令行参数会以文本字符串的形式存储在sys.argv中.并且sys.argv的长度至少为1,因为他的第一个元素是希望运行的python源文件名.其余的参数会存储在sys.argv[i]中,其中i大于等于1.

和C一样的,python的sys模块中也存储着输入输出和错误文件的变量,如下所示

```python
import sys
sys.stdout # print输出的文件位置
sys.stderr # 错误和traceback输出的文件位置
sys.stdin # 输入文件的位置
```

同样,标准输入输出也可以通过重定向的方式来重新把输入输出的位置移动到期待的位置.

```shell
python prog.py > text.txt
cmd1|prog.py|cmd2
```

第一个语句会把prog.py的输出重新输出到text.txt上;第二个语句则是cmd1的输出会作为prog.py的输入,而prog.py的输出则会导出给cmd2.这里我们用prog.py直接可以运行,并没有调用解释器.这是因为我们在python文件的开头调用了#!命令,如下所示,

```shell
#! /usr/bin/env python3
```

系统在读取到这一行指令的时候,会自动搜索用户环境变量中的python3解释器并调用.需要注意的是这个命令在Unix环境下生效,在Windows下效果并不是很好.而且这里如果希望可以让python源文件自动执行,在执行之前需要用chmod命令给他赋予可执行权限

```shell
chmod +x source.py
```

对于命令行编译python文件,我们还可以手动修改命令行的环境变量.但这个并不是python的语法,而是shell语法.但对于某些需要移植的程序而言,是十分重要的,因此我们在此对他加以介绍.

```shell
setenv variable value
setenv PATH /usr/local/bin:$PATH
```

第一条式子是设置环境变量的通用式,他只对当前shell进程和子进程生效,如果关闭了当前的shell进程,那么这些环境变量就会恢复默认值.第二个则是一个例子,我们发现他赋的值是并不是一个单独的值,而是在已有的PATH前面加上了一个环境,这里的:是用来分隔环境目录的,我们比较常用的就是在PATH前面加上一个值,如果把:放在$PATH后面那就是在已有的PATH后面加上一个环境.但这里我们不推荐使用

```shell
setenv PATH /usr/local/bin
```

这个语句会使得在这个shell里的环境变量被完全覆盖可能会有一些意想不到的错误.python中提供了一个字典来存储环境变量,如下所示

```python
import os
os.environ # 字典
```

Python的程序退出除了正常运行完成,就是通过异常抛出的方式.给出如下的异常抛出方式

```python
raise SystemExit
raise SystemExit(exitcode)
raise SystemExit('Information statements')
```

这里的exitcode只有零值的时候表示程序正常执行,对于非零值,都表示程序运行出错.除了通过raise抛出异常,还可以选择使用python的sys模块的exit方法实现.

```python
import sys
sys.exit(code)
```


<a id="org1832b0f"></a>

##  Design Discussion

本节有个比较有趣的程序的类型推断风格:鸭子类型.他一般用于动态语言或某些静态语言(Golang).静态语言的特点是在程序执行之前,代码编译时就可以知道所有变量的类型和方法返回值类型等.因为静态语言声明变量需要附带类型信息, 其是一块内存区域,

```C++
#include<stdio.h>
#include<string.h>
int main()
  {
    int x=10;
    x="ss";
  }
```

例如上面这个代码在代码编译阶段就会报错.静态语言的优点是代码结构非常规范,便于调试,但有时候会显得很罗嗦.

动态语言则是只有程序运行到这一行,程序才知道变量的类型.变量不需要在一开始声明变量的类型,本身也不会携带类型信息,他只与赋值的对象有关.其优点在于方便阅读,不需要写很多类型相关的代码,但其缺点在不方便调试,如果命名不规范容易出现阅读困难,不利于理解. 而鸭子类型指的是如果一个动物走起路来像鸭子,叫声也像鸭子,那么他就是鸭子.这样说来可能很抽象,其实鸭子类型就是动态类型语言的一种设计风格.一个对象的特征不是由父类决定,而是通过对象的方法决定.也就是我们并不关心对象的类型是什么样子的,我们只关心他的方法行为是什么结果.例如如下的代码,

```python
def max(a,b):
    if a>b:
        return a
    else:
        return b
max(2,3)
max('2','3')
```

上面的代码他都可以正确的比较整型和字符类型,对于这个函数而言,我们不关心输入的类型是什么,我们只关心是否能够运行,结果是否正确.
