---
title: Practical Python-Class
date: 2025-12-15 15:14:04
tags:
    - Computer Science
    - Python
categories: Python
mathjax: true
---

本笔记完全基于David Beazley的Python教程-[Practical Python](https://dabeaz-course.github.io/practical-python/Notes/Contents.html).

### Introducing Classes

面向对象编程(Object Oriented Programming)指将代码用对象组合的方式拆分.其中对象中包含数据(属性)和行为(应用在对象的方法).Python提供了class语句用来定义新对象,

```python
class Point:
  def __init__(self,x,y):
    self.x=x
    self.y=y
  def move(self,dx,dy):
    self.x+=dx
    self.y+=dy
```

这里Python作为动态语言,与C++最为不同的一点是,Python的类属性可以在程序运行中随意添加,但是很不推荐这么做,会让程序显得十分杂乱.

<!--more-->

在进行后续的讨论之前,我们先介绍一下Python中类的两种属性:实例属性和类属性.

1.实例属性主要是在\_\_init\_\_初始化函数中利用self.name的方式定义.其特点为对象实例的数据独立,也就是不同的实例是不能互相调用对方的数据;本质上实例属性是对象的一个字典项,默认是存储在\_\_dict\_\_里面的;变量类型不固定,可以在程序运行中动态修改.

```python
class Player:
  def __init__(self,x,y):
    self.x=x
    self.y=y
    self.health=100
    def move(self,dx,dy):
      self.x+=dx
      self.y+=dy
    def left(self,amt):
      self.move(-amt,0)
    def damage(self,pts):
      self.health-=pts
```

2.类属性.这种属性是直接写在类体定义里面,这种属性不属于某个特定的实例,而是属于类的本身.在初始化函数中,调用类属性的方式与前面的self.name不同,而是需要用class.name的方式调用.

```python
class Player:
  counter=0
  def __init(self,x,y):
    self.x=x
    self.y=y
    Player.counter+=1
```

类属性可以在任何实例化对象中调用.其特点是所有实例对象都可以调用同一个值;类属性可以被任何实例访问,但是实例属性是可以命名与类属性同名的变量,这样的话他就会覆盖类属性,无法在该实例中调用相关类属性.

这里我们简要提到一下C++的类结构,与上述Python的类结构进行对比.

```C++
class MyClass{
public:
  int a;
  double b;
  static int counter;
}
  int MyClass::counter=0
```

这里的静态成员变量不属于对象,而属于类本身,任何对象都可以调用其值,这个和刚刚介绍的Python的类属性一样.而且在类结构中所使用的static int counter语句只是一个变量声明,并没有分配变量内存空间.因此需要在类外做一个变量定义和初始化语句.值得注意的是对于静态成员变量必须要放在类外做定义初始化.C++类的特点为类型固定,其内部变量类型和数量均在编译时确定;访问受限由private/protected/public控制;静态成员共享.

在上面的C++类结构中,其可利用private做代码封装,类外无法随意访问private成员.而Python中并没有真正意义上的private变量,我们前面定义的类成员都可以在任意情况下被调用.但Python中提供了另一种解决方法

```python
class BB():
  def __init__(self,name):
    self.__name=name
  def get_name(self):
    return self.__name
```

这个\_\_开头的变量并不能通过类.\_\_name的方式调用,下面的代码可以展示

```python
b=BB('bb')
d=BB('dd')
b.__name='cc'
print(b.__name) # 'cc'
print(b.get_name()) # 'bb'
print(d.get_name())
print(d.__name) # 报错
```

这是因为虽然我们声明初始化的是\_\_开头的变量,但在Python的执行中会将其改变为\_类名\_\_属性名的方式,

```python
print(d._BB__name)
```

所以其实他还是可以被调用的,只是他不能通过用定义的名字调用而已.

我们为了后续的代码编写的规范,我们提供一个stackoverflow上提及的常用的程序规范.

1.  \_\_foo\_\_: 用于Python内部的名字,用来区别其他的用户自定义命名
2.  \_foo: 约定指定变量是私有的,不应该用from module import 的方式来导入,其余性质与公用变量一致.
3.  \_\_foo: 这个是Python程序中具有真实含义的作用,Python会将其变成\_类名\_\_name的变量名.

类可以视作一组对实例执行各种操作的函数.实例则指代码中实际操作的对象.实例方法指对对象实例的方法.如果实例方法中需要处理对象中的属性,那么对象本身一般以第一个参数的方式传输.虽然我们常见的传输对象本身使用的是self,不过实际上这个只是约定俗成的约定,可以用其他的.这是因为类只是创建属性的容器,而不是变量的查找域,换言之,虽然我们在类当中定义了某些属性,但是我们并不能在实例函数中直接使用变量名的方式调用,我们应该选择用类.变量名的方式调用.


<a id="org5bd1a9f"></a>

### Inheritance

继承则可以对现有的对象做特殊化修改.

```python
class Parent:
  pass
class Child(Parent):
  pass
```

这里我们称Child类为子类,派生类.Parent类为基类,超类.

继承可以认为是对曾经代码的扩展,一般用于添加新方法,重新定义已有方法或者添加新属性.

```python
class Stock:
  def __init__(self,name,shares,price):
    self.name=name
    self.shares=shares
    self.price=price
  def cost(self):
    return self.shares*self.price
  def sell(self,nshares):
    self.shares-=nshares
class Mystock(Stock):
  def panic(self):
    self.sell(self.shares)# 添加新方法
  def cost(self):#重新定义已有方法
    actual_cost=super().cost()
    return 1.25*actual_cost
```

上面的代码中提到了super.method().这个super()表示这个子类的父类,因此super.method()实际上就是调用父类的方法,可以用这种方法调用已有方法的不同版本.

我们介绍在子类中定义新属性的方式,

```python
class MyStock(Stock):
  def __init__(self,name,share,price,factor):
    super().__init__(name,share,price)
    self.factor=factor
  def cost(self):
    return self.factor*super().cost()
```

首先Python的变量必须初始化,因为他是一个动态语言,如果存在一个变量但他没有被赋值,程序是不可以为他分配内存空间的,所以我们如果希望在子类中添加新属性,我们其实需要重写子类的初始化函数,这里我们不对父类初始化的方式修改,就可以用super().\_\_init()的方式来初始化父类属性.

继承可以认为是组织某类相关对象的架构方式.

```python
class Shape:
  pass
class Circle(Shape):
  pass
class Triangle(Shape):
  pass
```

继承的作用一般是用于构建可重用,可扩展的代码框架.如先定义一个类框架,也就是基类,他可以提供一个通用的方法,通过继承基类的方式,我们对子类做特殊化定制的部分.

类似于基本类型,我们也可以用isinstance的函数来判断类的关系.

```python
class Shape:
  pass
class Circle(Shape):
  pass
c = Circle()
print(isinstance(c, Circle))   # True
print(isinstance(c, Shape))    # True
print(isinstance(c, object))   # True
print(type(c) is Circle) # True
print(type(c) is Shape) # False
print(type(c) is object) # False
```

从上面的代码中,我们可以发现isinstance(object,Class)判断obj是否为class或其任意子类的实例.type方法则是用于精确判断类的属性,他不会考虑类的包含关系,而isinstance是一种判断类的包含关系.isinstance方法用于判断对象是否可以被视作某个类型.

子类存在如下的Liskov Substitution Principle(LSP,里式替换法则):子类对象必须能在任何需要父类对象的地方被替换使用,而不破坏程序的正确性.

如果这个类没有父类,其实可以认为object为他的父类.

```python
class shape(object):
  pass
```

object可以视作所有对象的父类.
