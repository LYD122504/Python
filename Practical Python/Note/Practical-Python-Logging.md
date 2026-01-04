---
title: Practical-Python-Logging
date: 2026-01-04 15:58:00
tags:
    - Python
categories: Practical Python
mathjax: true
---

本笔记完全基于David Beazley的Python教程-[Practical Python](https://dabeaz-course.github.io/practical-python/Notes/Contents.html).

## Logging,error handling and diagnostics

logging模块解决的是一个工程级别的诊断信息管理问题:如何在不污染业务逻辑的前提下,记录那些对程序分析有用的信息,并且允许用户自行决定是否查看这些信息.这个之前我们其实也有一些做法,我们将其罗列在下面的表格

| 做法    | 问题                       |
| ------- | -------------------------- |
| print() | 无级别,无法关闭,无法重定向 |
| pass    | 丢失执行信息,丢失诊断信息  |
| logging | 可分级,可配置,可集中管理   |

所以对于日志模块而言,强调的是行为(记录日志)和策略(如何输出)分离.因此logging的设计是分层的,其中有Logger,Handler,Formatter和Filter.

<!--more-->

我们从Logger出发,讨论日志模块.logging提供了getLogger函数来返回一个logging.Logger对象,

```python
import logging
log=logging.getLogger(__name__)
```

这里的\_\_name\_\_是模块名,每个模块都有自己的log,如果getLogger同名,那么他其实是返回的同一个对象,因为Logger是按照名字全局缓存,并且可以通过名字共享配置.一个Logger实例其实代表日志命名空间的一个节点,他并非一个临时对象,而是一个长期存在且可复用的单例式对象.这些Logger会构成一个日志的命名树.Logger的日志等级的显示方式并不一定是打印在屏幕,而是受其内部配置决定.常见的日志等级如下所示

| 级别     | 用途           |
| -------- | -------------- |
| CRITICAL | 程序无法继续   |
| ERROR    | 操作失败       |
| WARNING  | 异常但可以继续 |
| INFO     | 关键运行信息   |
| DEBUG    | 细节诊断信息   |

一般来说,默认输出是WARNING以上的警告信息.其常见用法为

```python
import logging
name=__name__
log=logging.getLogger(name)
log.debug("Debug message from %s", name)
log.info("Info message from %s", name)
log.warning("Warning message from %s", name)
log.error("Error message from %s", name)
log.critical("Critical message from %s", name)
```

上面的这些日志代码并不负责调整日志输出的形式,如果我们需要自定义一些日志配置,可以利用basicConifg函数来修改.

```python
# main.py
import logging
logging.basicConfig(
    filename='app.log',
    level=logging.WARNING,
    format='%(levelname)s:%(name)s:%(message)s'
)
```

上面的代码一般出现在程序开头,用于告诉程序把日志写到哪里,写多少,怎么写.如果我们不做任何操作,那么默认的level是WARNING,输出的地方是stderr.我们也可以精确的控制某个特定的版块,

```python
logging.getLogger('fileparse').setLevel(logging.DEBUG)
```

只打开fileparse日志的debug播报等级.

Logger用于接受日志事件,那么Handler决定往哪里写,Formatter决定写入的形式,Filter决定要不要写.Handler是日志的输出通道.他负责回答这个日志写到哪里,如终端,文件,缓冲区等.常见的Handler类型如下所示

| Handler                 | 作用                   |
| ----------------------- | ---------------------- |
| StreamHandler           | 输出到流(默认是stderr) |
| FileHandler             | 输出到文件             |
| RotatingFileHandler     | 文件滚动               |
| TimeRotatingFileHandler | 按时间滚动             |

```python
import logging
logger = logging.getLogger("demo")
logger.setLevel(logging.DEBUG)
# Handler 1：终端
h1 = logging.StreamHandler()
h1.setLevel(logging.INFO)
# Handler 2：文件
h2 = logging.FileHandler("app.log")
h2.setLevel(logging.WARNING)
logger.addHandler(h1)
logger.addHandler(h2)
logger.debug("debug")
logger.info("info")
logger.warning("warning")
```

如果我们同时给logger配置了多个Handler.同一条日志被赋值并且依次发送给每一个满足条件的Handler.其余的RotatingFileHandler表示当日志文件满足某个条件,当前文件被封存并重命名,新的日志写入一个全新的文件.

```python
from logging.handlers import RotatingFileHandler
handler = RotatingFileHandler(
    "app.log",
    maxBytes=1024,     # 单个文件最大字节数
    backupCount=3      # 最多保留多少个旧文件
)
```

其可以限制单个日志文件的大小,同时保留历史日志,他能够保存一共n+1个日志,RotatingFileHandler主要是基于文件大小做一个轮转.而对于TimeRotatingFileHandler则是基于时间做轮转.

```python
from logging.handlers import TimedRotatingFileHandler
handler = TimedRotatingFileHandler(
    "app.log",
    when="D",       # 每天
    interval=1,
    backupCount=7
)
```

这里的when关键字决定轮转的时间单位,上面的when="D",interval=1,表示每天轮转一次,如果考虑when='H',interval=6,那么就是每六小时轮转一次.如果超过了backupCount,那么最旧的文件就会被自动删除.TimeRotating并不是实时记录器,他只发生在当前时间越过轮转点.

Formatter则是决定记录的日志应该是以什么形式写入.其主要的调用方式如下

```python
formatter = logging.Formatter(
    "%(levelname)s:%(name)s:%(message)s"
)
```

这里面常用的字段为

| 字段          | 含义      |
| ------------- | --------- |
| %(levelname)s | 日志级别  |
| %(name)s      | logger 名 |
| %(message)s   | 日志内容  |
| %(asctime)s   | 时间      |
| %(filename)s  | 文件名    |
| %(lineno)d    | 行号      |

Formatter并不是挂载在Logger上,而是挂载在Handler上.

```python
handler.setFormatter(formatter)
```

Filter则是对日志做一个筛选,考虑是否需要将这个信息写入日志,和前面提到的播报level不同的是,Filter可以基于任意的条件.

```python
class MyFilter(logging.Filter):
    def filter(self, record):
        return "password" not in record.getMessage()
```

这里返回值True表示通过,False表示拦截.Filter则是既可以挂载在Logger上,也可以挂载在Handler上.

```python
logger.addFilter(...)
handler.addFilter(...)
```

如果挂载在Logger上,那他会自动作用在所有的Handler上.如果挂载在Handler上,那他只会作用在这个Handler.

给一个完整的代码

```python
import logging
import sys
# 基本配置
logging.basicConfig(
    level=logging.WARNING,  # 兜底级别
    format="%(levelname)s:%(name)s:%(message)s"
)
# 构造过滤器类
class IgnoreKeywordFilter(logging.Filter):
    #->表示设计上应该返回什么类型,提高可读性
    #record:logging.LogRecord表示参数类型注解
    #表示record这个参数在设计和语义上应当是一个logging.LogRecord对象
    def filter(self, record: logging.LogRecord) -> bool:
        return "ignore" not in record.getMessage()
# 创建Logger对象
logger = logging.getLogger("demo.app")
logger.setLevel(logging.DEBUG)  # Logger 总闸门
# 如果True,会调用logger的handler之后,再去调用root logger
logger.propagate = False        # 避免重复输出到 root logger
# 创建新的formatter
console_formatter = logging.Formatter(
    fmt="%(levelname)s - %(message)s"
)
file_formatter = logging.Formatter(
    fmt="%(asctime)s [%(levelname)s] "
        "%(name)s %(filename)s:%(lineno)d - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
# 创建不同的Handler
# 控制台 Handler
console_handler = logging.StreamHandler(sys.stderr)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(console_formatter)
console_handler.addFilter(IgnoreKeywordFilter())
# 文件 Handler
file_handler = logging.FileHandler("app.log", mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(file_formatter)
file_handler.addFilter(IgnoreKeywordFilter())
# 绑定 Handler 到 Logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
def main():
    logger.debug("This is a DEBUG message")
    logger.info("Application started")
    logger.warning("Low disk space")
    logger.error("Something went wrong")
    # 这条会被 Filter 丢弃
    logger.warning("This message should be ignored")
    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception("Unhandled exception occurred")
if __name__ == "__main__":
    main()
```

<a id="org27ec2d3"></a>
