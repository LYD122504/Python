---
title: Pracitcal Python-Multiple Inheritance and MRO
date: 2025-12-18 15:41:08
tags:
    - Python
categories: Practical Python
mathjax: true
---

## Multiple Inheritance and MRO

继承是面向对象编程中用于建立类型层次关系的机制.子类(subclass)继承父类(superclass)的属性和方法;子类对象可以被当做父类对象使用.

```python
class Parent: pass
class Child(Parent): pass  
```

其在程序设计中的作用:代码复用;抽象公共接口;建立类型约束.

<!--more-->

多重继承则指的是一个类可以同时继承自多个父类.

```python
class A: pass
class B: pass
class C(A,B): pass
```

上述代码表示类C继承类A和类B.类C同时具有类A和类B的接口和行为.多重继承通常用于组合多个相互独立的功能,而非单一的层级抽象.其父类的特点为结构简单;状态较少;不表达本质类型,而表达附加类型.

虽然我们前面这么介绍多重继承,但是实际应用中多重继承的继承结构十分之复杂,我们将其简要分为下面三类:线性结构,树状结构,菱形结构.

线性结构,本质上来看其实就是单继承结构.他的优点在于方法查找路径唯一,不存在父类歧义或父类冲突.单继承强调本质类型,结构清晰,语义稳定,行为可预测.代码如下

```python
class A: pass
class B(A): pass
class C(B): pass
```

<img src="https://github.com/LYD122504/picx-images-hosting/raw/master/20251217/屏幕截图-2025-12-17-160655.1ziq02kiyc.png"
     alt="屏幕截图-2025-12-17-160655"
     style="display: block; margin: 0 auto; zoom: 50%;" />

树状结构,与前面的单继承不同,树状结构源自多重继承.Mixin是Python中常用的设计模式,用来给类附加功能,而不依赖于深层次的继承体系. Mixin是一种特殊的类,其只提供某种功能或方法,不单独表示一个独立对象类型,其主要目的是混入其他类中增强功能.其特点为通常不独立实例化;提供可复用的功能;组合多个Mixin类与主类形成新类. Mixin的设计原则为功能单一,一个Mixin只提供一个特定功能;不独立,不能单独实例化;组合使用,与其他Mixin类或主类组合,实现多功能组合.Mixin的实现依赖于Python支持的多继承机制.

<img src="https://github.com/LYD122504/picx-images-hosting/raw/master/20251218/2025-12-18_12-51-13_screenshot.3ns2ynruf9.png"
     alt="2025-12-18_12-51-13_screenshot"
     style="display: block; margin: 0 auto; zoom: 50%;" />

 我们给出一个Mixin的典型例子,来表示他的作用是增强类的能力.

```python
class LogginMixin:
def log(self,msg):
    print(f"[LOG]:{msg}")
class AuthMixin:
def authenticate(self,user):
    print(f"Authenticating {user}")
class User(LogginMixin,AuthMixin):
def __init__(self,name):
    self.name=name
    u=User('Alice')
    u.log("User created")
    u.authenticate("Alice")
```

第三种情况也是多重继承中最为复杂的菱形继承情况,我们先给出他的继承图结构如下:

<img src="https://github.com/LYD122504/picx-images-hosting/raw/master/20251218/2025-12-18_12-56-13_screenshot.64ebdkyqbq.png"
     alt="2025-12-18_12-56-13_screenshot"
     style="display: block; margin: 0 auto; zoom: 50%;" /> 

他面临的问题是类D继承自类B和类C,但是类B和类C都是继承自类A,也就是说在这一个继承体系下类A被继承了两次.所以就会如下几个问题需要解决,如果我们调用A的函数,是否需要调用两次?如果我们调用B和C中的同名函数,是会先调用B的还是C的?D的继承逻辑是否会影响B和C的继承逻辑?

为了方便,我们先给出一套菱形继承的代码.我们将基于这个代码解释上述的三个问题.

```python
class A:
def foo(self):
    print("Here is a A")
class B(A):
def foo(self):
    print("Here is a B")
    A.foo(self)
class C(A):
def foo(self):
    print("Here is a C")
    A.foo(self)
class D(B,C):
def foo(self):
    print("Here is a D")
    B.foo(self)
    C.foo(self)
    d=D()
    d.foo()
```

我们希望的是在运行中类A只被调用一次,且类D不会影响类B和类C的继承顺序,并且有一个明确的方法调用顺序.在Python中这一方法解释顺序(MRO),他是存储在类中的\_\_mro\_\_属性中的.我们调用类D中的函数,会先在MRO中依次查找,直到第一次查找到同名函数,就会将其调用,并不会多次调用.这里我们从他的演变开始慢慢介绍其背后的C3线性化算法.

对于继承结构图,我们可以认为其实就是一个有向无环图(DAG),而MRO实际上就是对有向无环图做一个拓扑排序.因此我们很自然的想到使用DFS或者BFS算法,我们在此选用DFS算法作为我们例子,这也是比较早的合乎我们直观的方法解释顺序.其代码如下所示.

```python
def old_mro(cls,order):
    order.append(cls)
    for base in cls.__bases__:
        old_mro(base,order)
    return order
```

这里我们用到了一个类的\_\_base\_\_属性,他会存储当前类的父类列表.整个代码结构是通过利用递归的方式,一直走到没有父类了返回.但是这个算法有一个缺陷就是如果我们对上面的菱形结构做这个方法会发现他其实导出的MRO为DBACA,A在这一解释下被调用了两次,这与我们期待的并不一致,所以我们需要对这个方法做一些改动.

我们发现上面的MRO中A出现了两次,所以呢,我们很自然的想到可以先对继承图做一个DFS算法,然后对得到的结果做一个去重操作,只保留最后出现的位置.代码如下.

```python
def improve_mro(cls,order):
    mro=old_mro(cls,order)
    dmro=[]
    dmro.append(mro[-1])
    mro.reverse()
    for item in mro:
        if item in dmro:
            continue
        dmro.append(item)
        dmro.reverse()
    return dmro
```

在这个代码下我们发现他是可以把前面的菱形结构的顺序记作DBCA的,这是合乎我们前面希望的,但他其实在保证继承单调性上是存在问题,单调性也就是指的是类B继承的顺序不会因为某个子类继承了以后会发生变化.如下所示,但是这个代码并不能在Python中运行,因为他不满足单调性,但是我们这个算法并没有涉及单调性检验,所以我们只是在形式上给与一个反例:

```python
class D: pass
class E: pass
class B(D,E):pass
class C(E,D):pass
class A(B,C):pass
```

这里我们可以看出B的继承顺序为BDE,C的顺序为CED,如果我们用DFS算法计算A的MRO为ABDECED,再对他进行降重发现得到的MRO为ABCED,对C而言他的继承顺序没问题,但是B的继承顺序被改了,所以与单调性矛盾.

在这些基础上,现行的Python选择使用了C3线性算法作为MRO计算的算法. C3线性化算法来自于他实现符合三种重要的性质:一致性扩展优先图(EPG),保留局部优先次序和适合单调性准则.

EPG:在一般意义下,优先图就是一张有向图,节点表示对象,边XY表示一种优先约束:X必须在Y前面,所以优先图其实就是一个偏序关系的图表示.在偏序理论中如果我们已经有了一个偏序关系,我们希望能够获得一个全序关系,且这个全序关系不会破坏原有顺序,这样的全序关系我们称之为一致性扩展,比较典型的例子就是对DAG做拓扑排序.所以EPG其实就是用有向图表示的一组优先约束,并要求寻找一个保持这些约束的一致性扩展.在多重继承中,EPG的节点是类,优先约束就是继承关系,父类要比子类出现早.C3 的目标就是在这个 EPG 上,找到一个一致性扩展作为子类的MRO.

保留局部优先次序:在一般系统设计中,表示在一个局部上下文中显式给出的顺序约定在更大的系统中必须得到尊重.这是语义一致性问题.在类定义中我们有A(B,C)这并不是一个可以随意更改的顺序,而是表示在继承关系中B的优先级高于C.因此,我们期待合法的MRO可以满足B在C前面.

适合单调性准则:在数学中,单调性指的是在某个序结构下,扩展或演化并不会破坏原有的相对顺序.在多重继承中,单调性表示子类的MRO必须是父类MRO的一致性扩展,也就是父类已经确定的顺序在子类中仍然能够成立.

综上来,多重继承的C3线性化本质上是在一个由局部优先次序和父类顺序共同诱导的优先图上,寻找一个满足单调性的一致性扩展.这个一致性扩展也就是我们想要的MRO.

C3的核心结构其实就是一个递归结构和merge函数设计.对于任意类C,他的线性化表示C+merge(父类线性化,父类列表),我们用公式的形式给出这一表示, 
$$
L(C)=[C]+merge(L(P_1),L(P_2),\cdots,[P_1,P_2,\cdots])
$$
其中$P_1,P_2,\cdots$是C的直接父类.merge函数则是一个受约束的拓扑排序过程,他试图在多个已排序的序列中,逐步选出一个合法的下一个元素.其关键步骤在于每一步中先选取第一个元素的首元素作为候选元素,判断这个元素不出现在任何其他序列的尾部,如果成立,那么他就将其加入结果并且在所有序列中将其删除,如果不成立,就看下一个元素的首元素作为候选元素,直到元素都被遍历,若仍没有合法的MRO,那么抛出异常.

```python
def merge(seq):
    result=[]
    while True:
        # 把空列表去掉
        seq=[seqs for seqs in seq if seqs]
        # 如果seq序列空了,也就是没有问题完全输出了
        if not seq:
            return result
        for seqs in seq:
            flag=seqs[0]
            if not any(flag in item[1:] for item in seq):
                break
        else:
            raise  TypeError("Inconsistent hierarchy, no C3 MRO possible")
        result.append(flag)
        # 在序列里面把他删掉
        for item in seq:
            if item and item[0] == flag:
                item.pop(0)
def C3Mro(cls):
    # 父类序列
    Base=cls.__bases__
    # 父类线性化
    BaseLinearSeq=[list(C3Mro(base)) for base in Base]
    BaseLinearSeq.append(list(Base))
    return [cls]+merge(BaseLinearSeq)
```

这里用到了一个尚未提到的代码结构for&#x2026;else&#x2026;他的意思是如果在for循环中出现了break,那么跳过else继续运行,如果没有break,那就进入else运行.any函数则表示如果可迭代对象iterables中任意存在一个元素为True,则返回True;如果迭代对象是空那么返回False.与之相对的是all函数,如果可迭代对象iterables中所有元素都为True则返回True;若迭代对象为空,则返回True.

检测C3算法的例子

```python
class D: pass
class E: pass
class F: pass
class B(D,E):pass
class C(D,F):pass
class A(B,C):pass

print(Mro.C3Mro(A))
```

<a id="org346572a"></a>
