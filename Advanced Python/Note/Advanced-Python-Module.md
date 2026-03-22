---
title: Advanced Python-Modules and Packages
date: 2026-03-22 16:36:09
tags:
    - Python
categories: Advanced Python
mathjax: true
---

# Modules and Packages


<a id="org7e8c577"></a>

## Modules

模块化和包机制是Python管理复杂性的核心手段,也是代码复用的基础.每个源文件都是一个模块,import用于加载并执行一个模块.我们在到如模块的同时也到入了其定义的命名空间.

```python
import foo
foo.grok()
# 相当于如下的调用方式
foo.__dict__['grok']()
```

<!--more-->

所以module的命名空间本质上就是一个字典,在主程序中可以用module.\_\_dict\_\_访问,这也意味着你可以在运行时动态修改模块的内容.模块文件中其实还有一些特殊变量定义,如\_\_file\_\_表示源文件名称,\_\_name\_\_表示模块名称,\_\_doc\_\_表示模块文档字符串.因为主程序其实也可以认为是一个模块文件,只不过他的模块名是main.上面提到的\_\_name\_\_属性是区分源文件是直接运行还是被导入执行的关键,如果文件是直接运行的,那么name就是main,而如果被导入的,那么name就是模块文件名,这就是编写可复用模块的标准模式.

我们在此简要介绍一下模块导入的流程,以如下的伪代码解释,

```python
import types
def import_module(name):
    # 定位模块文件并获取源代码
    filename=find_module(name)
    code=open(filename).read()
    # 创建enclosing模块对象
    mod=types.ModuleType(name)
    # 运行源代码
    exec(code,mod.__dict__,mod.__dict__)
    return mod
```

源代码在模块字典中通过exec执行,存储的内容就是执行完exec的结果.所以导入的机制为寻找模块文件,创建一个新的模块对象,在该对象的命名空间的字典中执行文件代码.所以模块文件的全局变量实际上会变成模块对象的属性.import语句将模块对象插入到导入模块的文件所使用的字典.其流程是先加载和执行模块,然后创建一个模块变量,指向这个模块对象.每个模块都只会加载一次,重复import就只会返回之前加载过的以前模块的引用.

```python
import sys
print(list(sys.modules))
```

sys.modules指的是所有已经加载模块的字典.模块是一个单例模式,如果在不同地方多次导入,它们指向的是内存中同一个模块对象,这也意味着模块级的全局变量在所有调用文件之间是共享的.我们在此简单的引入模块的单例模式,其伪代码如下所示,

```python
import types
import sys
def import_module(name):
    # 检查模块缓存
    if name in sys.modules:
        return sys.modules[name]
    filename=find_module(name)
    code=open(filename).read()
    mod=types.ModuleType(name)
    exec(code,mod.__dict__,mod.__dict__)
    return mod
```

我们通过如下代码选择性导入模块中的一部分变量,适用于频繁适用的变量名,

```python
from module import var
```

但这不会改变导入的工作方式,模块依旧会被加载和执行,然后会在程序中复制变量名,大体如下所示,

```python
grok=sys.modules['foo'].grok
```

我们可以用如下代码获取模块中的所有代码并将它们放入调用文件的命名空间,

```python
from module import *
```

但他只适用于不以\_开头的变量,所以我们可以用\_name来定义模块中不想被导入的值.需要提醒的是import \*被视作一个编程的坏习惯,其污染了当前命名空间,使代码来源不清晰,而以下划线开头的名称被视为私有,不会被通配符导入.

在上面我们提及了模块不可以被重复加载,但是实际上我们可以调用importlib使得模块可重新加载.

```python
import importlib
importlib.reload(foo)
```

<a id="org5e98ebd"></a>

## Packages

Python库的标准做法是组织为位于顶层包名下的分层模块集,如下所示,

<img src="https://github.com/LYD122504/picx-images-hosting/raw/master/20260322/2026-03-21_13-52-19_screenshot.41ymfwjtbv.png" style="zoom:50%;" /> 

这样的层次命名结构可以避免在大型程序中的命名冲突.为了创建Python中的包,应该先创建模块库的层次结构,将文件组织在具有所需结构的目录中,

<img src="https://github.com/LYD122504/picx-images-hosting/raw/master/20260322/2026-03-21_14-05-35_screenshot.5j4rhnny2k.png" style="zoom:50%;" />

 这里我们可以看见创建包在每个目录文件中创建\_\_init\_\_.py,这个文件可以是空的,但是必须要存在.他的存在会告知Python解释器该目录应该视作一个包.一旦我们设置了init.py,那我们就可以使用import语句导入包.

```python
import packagename.foo
import packagename.parsers.xml
from packagename.parsers import xml
```

几乎所有内容的工作方式与以前一样,只是import语句会具备多层级别.这里我们需要注意到子模块的相对导入会失效,也就是

```python
# spam/
#     foo.py
#     __init__.py
#     bar.py
# bar.py
import foo # Fails
```

所以这可以解决了顶层包和子模块之间的名称冲突,

```python
# bar.py
import os
```

这里import导入方式是绝对的,从顶层开始往下查找的.在包内部,直接使用import语句会被是做绝对导入,他会在sys.path查找系统级的包,而不是在同级目录下查找,这样可以避免包内模块意外覆盖标准模块.我们需要用绝对导入的方式来获取包内模块,它需要调用顶层包的名称,

```python
from spam import foo
```

但这样如果我们修改包结构的话,那么这样的绝对导入就需要修改整体的代码,因此Python又提供了包相对导入的方法,其中.表示当前包,..表示父包.

```python
# bar.py
from . import foo # Imports ./foo.py
from .foo import name # Load a specific name
from .grok import blah # Imports ./grok/blah.py
```

相对导入使得包内部重构更容易,但只能在包内使用,不可以用作顶层脚本的直接导入.包内也会定义一些有用的特殊变量,如\_\_package\_\_为封装包的名称,\_\_path\_\_则是子模块的搜索路径,

```python
import xml
print(xml.__package__)
print(xml.__path__)
```


<a id="org6e82cfb"></a>

## \_\_init\_\_ File

\_\_init\_\_.py的主要用途是将多个源文件缝合到一个顶层导入中.\_\_init\_\_.py是包的入口,不仅标记目录为包,还可以执行初始化代码,或者导出子模块的内容,简化用户的段数路径.

```python
# foo.py
class Foo:pass
#bar.py
class Bar:pass
#__init__.py
from .foo import Foo
from .bar import Bar
# main.py
import spam
f = spam.Foo()
b = spam.Bar()
```

用户会只看到一个统一的顶层包,将跨子模块的拆分隐藏起来.这是一个优秀的API设计模式,内部实现可以分散在多个文件中以方便维护,但对外只暴露一个简洁的接口.不仅如此,我们可以在子模块中定义\_\_all\_\_列表用于控制from module import \*传导的变量属性,可以隐藏一些子模块的内部实现,

```python
# foo.py
__all__ = ['Foo']
class Foo(object): pass
def func: pass
```

这样的话,如果在\_\_init\_\_.py中导入foo中的全部变量,其实只有类Foo,而没有func函数.所以\_\_all\_\_列表明确声明了模块的公共API.它不仅控制import \*的行为,也是给阅读代码的人看的文档,表明哪些内容是稳定的接口,哪些是内部实现.


<a id="orgba6baaa"></a>

## Main Module

上面的导入模块中,我们需要十分小心包内的循环导入,应该小心的遵循控制流,因此定义的顺序十分重要.例如A导入B,B导入A,模块执行完成前就会尝试访问一个未定义的内容,那就会报错.一般来说都是因为导入放在模块的顶部,如果需要改正这一问题一般是将导入语句放在不同的地方,避免循环依赖.将导入语句移动到函数内部或者类定义之后,可以出现延迟导入,避免执行时候的冲突.最好的解决方案通常是重构代码,将共享内容提取到一个单独的模块中,打破循环依赖.

将指定模块作为主程序运行,这样可以将支持的脚本或者应用程序封装在包里面.

```shell
python -m module
```

-m标志告诉Python查找模块并执行它,即使该模块在包内部.我们也可以为包提供一个主入口程序点\_\_main\_\_.py,使得包目录可以执行,这样的话我们可以直接使用python -m package,他会自动执行\_\_main\_\_.py,这样可以让包像前面的程序一样简单运行.
