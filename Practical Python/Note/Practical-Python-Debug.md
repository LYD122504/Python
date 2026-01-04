---
title: Practical Python-Debug
date: 2026-01-04 19:19:55
tags:
    - Python
categories: Practical Python
mathjax: true
---

本笔记完全基于David Beazley的Python教程-[Practical Python](https://dabeaz-course.github.io/practical-python/Notes/Contents.html).

## Debugging

调试的开始都是从Traceback开始.当Python程序方程未补货异常的时候,解释器就会打印Traceback(错误回溯),他包含调用栈(函数是如何一层层调用到出错位置的),精确的出错行号,异常类型和异常信息.

<!--more-->

```shell
Traceback (most recent call last):
  File "C:\Users\Liyaoda\Nutstore\1\Computer\Learned\Pratical_Python\Chapter8\demo\Ch8_Sec3.py", line 21, in <module>
    process()
  File "C:\Users\Liyaoda\Nutstore\1\Computer\Learned\Pratical_Python\Chapter8\demo\Ch8_Sec3.py", line 19, in process
    result = normalize(data)
             ^^^^^^^^^^^^^^^
  File "C:\Users\Liyaoda\Nutstore\1\Computer\Learned\Pratical_Python\Chapter8\demo\Ch8_Sec3.py", line 5, in normalize
    total = sum(values)
            ^^^^^^^^^^^
TypeError: 'int' object is not iterable
```

阅读Traceback的方式其实是从最后一行开始,因为最后一行是异常的直接原因,然后在慢慢向上回溯,从而可以了解错误是如何被逐层调用传播出来的.值得注意的是,异常点往往并不是错误发生的地方,而是错误暴露的地方.

如果我们直接用python解释器去处理含错误的程序,他遇到错误之后会崩溃并退出.但我们仍可以通过python -i的方式保留解释器运行.

```python
python -i Ch8_Sec3.py
```

他的含义是脚本执行完,即使是因为异常退出,解释器也不会退出,当前的作用域,变量,对象仍然存在.我们可以直接现场调用一些变量来检查程序内部状态.

```python
>>> x
>>> type(x)
>>> locals()
>>> globals()
```

本质上这等价于在C/C++崩溃后还能冻结现场,是一种轻量级事后调试.但是值得注意的是,-i他只能保留全局变量和定义的函数,类和模块,对于函数内部的局部变量是不能检查的.

虽然上面提到了一些调试方式,但实际上print仍然是最简单的调试方式.但是对于调试,更为建议的是选择使用repr()函数,因为repr函数返回的字符串会更为符合调试分析的精确表达.因为在调试过程中,我们更期待的是返回变量的类型,精度以及是否被隐式转换,如果直接print可能会被解释器做一些隐匿的美化,导致信息被隐藏.

上面的python -i只能检查全局变量的正确与否,我们可以用pdb来做交互式调试.在python3.7以上的版本,可以通过breakpoint()来直接调用pdb

```python
def some_function():
    ...
    breakpoint()
    ...
```

这里推荐使用breakpoint()的原因是可以通过环境变量切换调试器,不强耦合pdb.加了断点之后,程序运行到这个断点,运行停止,进入REPL和调用栈上下文,然后可以逐行执行,检查变量和修改状态.我们也可以直接调用调试器来运行程序,

```shell
python3 -m pdb Ch8_Sec3.py
```

程序从第一行就进入调试器.我们可以在程序中提前设断点,控制执行路径,检查初始化阶段的状态.pdb常见的命令如下所示

| 命令   | 含义                       |
| ------ | -------------------------- |
| w      | 查看当前调用栈（极其重要） |
| u / d  | 在调用栈中上下移动         |
| l      | 查看当前代码               |
| a      | 查看当前函数参数           |
| p expr | 打印表达式                 |
| s      | 单步进入                   |
| n      | 单步执行（不进入函数）     |
| c      | 继续运行                   |
| b      | 设置断点                   |

调试器实际上就是在时间轴,调用栈和函数局部状态三个调试维度上调试程序.设置断点的常用方式如下所示

| 命令         | 断点设置方式        |
| ------------ | ------------------- |
| b 45         | 当前文件第45行      |
| b file.py    | 指定文件的第45行    |
| b foo        | 当前文件的函数foo() |
| b module.foo | 模块中的foo()       |

实际上,按函数名下断点通常比行号更稳定.

<a id="org61aedbc"></a>
