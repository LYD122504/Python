---
title: Practical Python-Packages
date: 2026-01-04 19:21:32
tags:
    - Python
categories: Practical Python
mathjax: true
---

本笔记完全基于David Beazley的Python教程-[Practical Python](https://dabeaz-course.github.io/practical-python/Notes/Contents.html).

## Packages

任意一个python文件就是一个模块,这里的模块解决的是代码复用与命名空间隔离.

```python
# foo.py
def grok(x):
    pass
def spam(x):
    pass
# main.py
import foo
foo.grok(2)
```

但是在大型程序中,具有大量的模块文件,如果仍然通过模块管理代码,会使得主程序被大量的模块文件隐藏,因此对于大量代码组织架构的程序中,包代替模块成为管理代码的好方式.

<!--more-->

包实际上就是模块的集合加上层级命名空间,形式上来看,包就是一个目录以及\_\_init\_\_.py文件.包解决的问题是大规模代码的组织问题,模块名冲突问题,以及应用与库的结构分离问题.但如果我们只是简单的将模块文件放入包目录里面,那么程序的运行会立刻崩溃.这是因为包内模块之间的导入方式不同以及包内模块不能直接当做脚本运行.

我们常见的导入模块的方式为

```python
import fileparse
```

如果fileparse模块在包目录内,那么他就会报错,这是因为此时fileparse并不是顶层模块,而应该用pack.modules的方式调用.正确的导入方式可以简单的分为两种:绝对导入,不推荐使用在包内模块的互相调用

```python
from pack import module
import pack.module
from pack.module import func
```

他的缺点是将包名写死,如果我们在后续程序运行中修改了包名,那么就要逐一修改包名,比较麻烦.因此Python官方更为推荐的包内导入方式为相对导入

```python
#.表示当前包
#..表示上一级包
from . import module
from .module import func
```

相对导入只能用于包内模块,不能应用到顶层脚本.

包内模块不能直接当脚本运行,

```python
python porty/pcost.py
```

这是因为Python将porty/pcost.py当做孤立文件,sys.path中没有porty的父目录,所以相对导入和包结构就会全部失效.我们可以用python -m的方式来运行模块

```python
python -m porty.pcost
```

Python先把当前目录加入sys.path再以模块的方式执行,包结构完整可见.或者我们也可以用顶层脚本的方式调用,此时我们需要在和包目录同级的地方创建一个python文件并用如下代码调用,

```python
# print-report.py
import sys
from porty.report import main
main(sys.argv)
```

这里需要牢记脚本永远在包外,包内只放库代码.

包里面我们一开始创建了一个\_\_init\_\_.py,他并非一个占位文件,他的核心作用是声明这是一个包并且组织对外的API接口.

```python
# porty/__init__.py
from .pcost import portfolio_cost
from .report import portfolio_report
#main.py
from porty import portfolio_cost
```

这一个顶层文件的工程意义是控制用户应该看到什么,隐藏内部实现细节和提供稳定接口
