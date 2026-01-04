---
title: Practical Python-Testing
date: 2026-01-04 15:55:39
tags:
    - Python
categories: Practical Python
mathjax: true
---

本笔记完全基于David Beazley的Python教程-[Practical Python](https://dabeaz-course.github.io/practical-python/Notes/Contents.html).

## Testing

Python动态特性使得测试对大多数程序至关重要.编译器的静态编译并不能帮你查到程序错误,唯一发现错误的方式就是运行代码,并确保测试了他的所有功能.

<!--more-->

assert语句是程序的内部检查.如果表达式不为真,他就会引发一个AssertError异常.他的常用的语法是

```python
assert <expression> [, 'Diagnostic message']
```

一般来说,我们不会使用他来做用户输入检测.他的作用一般是用于程序内部检查和不变式(应该始终是真的条件)

Contract Programming(契约编程)或者也称之为Design by Contract(设计契约),广泛使用断言是设计软件的一种方法,他规定软件设计者应该为软件的组件定义精确的接口规范.如

```python
def add(x, y):
    assert isinstance(x, int), 'Expected int'
    assert isinstance(y, int), 'Expected int'
    return x + y
print(add(2,3))
print(add('hello',3))
```

这样的代码检查可以快速发现那些没有使用适当参数的参数.断言也可以做一些简单的代码测试,

```python
def add(x,y):
    return x+y
assert add(2,2)==4
```

这样我们就可以将测试和代码放在同一个模块中.这样的优点是如果代码有错误,那么导入模块就会直接报错崩溃.这其实有点像是常见的冒烟测试,冒烟测试是一种最基础,快速的验证性测试,用于确认系统或软件在经历一次构建,部署或重大修改之后,核心功能是否处于可用状态.它的目标不是发现细节错误,而是尽早暴露致命问题,以判断是否值得继续进行后续,更深入的测试.其主要特点在于

1.  覆盖面小但关键:只测试最核心,最重要的功能路径
2.  测试深度浅:不涉及复杂逻辑,边界条件或异常场景
3.  执行迅速:通常几分钟内完成
4.  结论明确:只有通过/不通过,用于决定是否继续后续工作

除了内置的assert检查,Python还有提供了unittest模块.

```python
# test_simple.py
import simple
import unittest
# Notice that it inherits from unittest.TestCase
class TestAdd(unittest.TestCase):
    def test_simple(self):
        # Test with simple integer arguments
        r = simple.add(2, 2)
        self.assertEqual(r, 5)
    def test_str(self):
        # Test with strings
        r = simple.add('hello', 'world')
        self.assertEqual(r, 'helloworld')
```

测试类必须要继承unittest.TestCase.每个测试函数都要以test开头.unittest也内置了一些断言,每个断言都对应着不同的情况.

| 断言语句                                | 作用                                                   |
| --------------------------------------- | ------------------------------------------------------ |
| self.assertTrue(expr)                   | 断言expr为真                                           |
| self.assertEqual(x,y)                   | 断言x等于y                                             |
| self.assertNotEqual(x,y)                | 断言x不等于y                                           |
| self.assertAlmostEqual(x,y,places)      | 断言x和y在小数点后places位内相等                       |
| self.assertRaises(exc,callable,arg1,..) | 断言调用 callable(arg1, arg2, &#x2026;)时会抛出exc异常 |

除了unittest模块外,其实还有一个pytest标准测试框架,他强调简洁,可扩展,可读性强.他的特点在于

1.  零样本:测试函数可以直接用test\_开头,不需要继承基类
2.  断言重写:使用原生的assert,失败给出结构化可读性极强的错误信息
3.  Fixture机制:用以来注入方式管理测试资源
4.  高度可扩展: 丰富的插件生态
5.  与unittest兼容:可以运行基于unittest.TestCase的测试

pytest 会自动发现:文件名为test\_\*.py或\*\_test.py的自动执行或函数名为test\_\*自动调用测试.

<a id="org9f65edf"></a>
