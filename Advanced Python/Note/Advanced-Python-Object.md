---
title: Advanced Python-Classes and Objects
date: 2026-02-05 23:31:38
tags:
    - Python
categories: Advanced Python
mathjax: true
---

# Classes and Objects

<a id="org704c65d"></a>

## Objects

面向对象编程其实就像是基于行为的自下而上的建模.一个对象则会包含一些内部状态和一些对内部状态的操作.因此,对于一个对象而言,其中包含的数据和行为是密不可分的,数据是对象的属性,而行为则是体现了对象的特性.

<!--more-->

Python中一般用class声明语句来定义一个新的对象.

```python
class Player:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.health=100
    def move(self,dx,dy):
        self.x+=dx
        self.y+=dy
    def damage(self,pts):
        self.health-=pts
```

从上面我们可以看出类其实是一系列的函数,从而提供对对象示例的不同的操作方式.这里我们需要强调的是,class声明语句只是提供了类的定义方式,并不提供一个可以操作的对象.在程序中,我们需要对类做实例化得到对象示例,才可以调用方法进行相关操作.

每个实例都具有他自己的局部数据,这个数据是每个实例单独占有的,其他的实例不能随意访问.实例数据的初始化一般是基于\_\_init\_\_函数,换言之任意存储在self对象的数值都是实例数据.对于实例属性的数量或类型没有任何限制.实例方法则是指应用在对象实例的函数,一般都是在类声明语句中已经给出了相关定义.这里需要注意的是实例方法的第一个参数一般都是对象.按惯例而言,实例一般会记为self,但这个只是一个习惯,并不是很重要,可以用其他的名字来代替.实例方法其实就是普通函数的定义,只是约定俗称将实例对象作为第一个参数 传入.

对象的属性指的是通过.来访问的.例如

```python
a.x # 实例属性
Player.move # 类属性
import math
math.pi # 模块属性
```

在Python中类本身并不会创建一个新的作用域,因此在类的方法内部调用其他方法时,必须显式地通过self来引用实例方法,否则Python会去全局作用域中查找同名函数,从而可能导致NameError或调用错误的函数.在Python中,作用域规则遵循LEGB(Local-Enclosing-Global-Builtin).类的代码块不是一个封闭作用域,类中定义的方法是独立的函数,他的局部作用域只包含自己的参数和内部变量,方法内部无法直接调用类中定义的其他方法或属性,除非通过self(实例)来访问.


<a id="org69ce5ba"></a>

## Manipulating Instances

对实例属性的操作一般是三个形式:

```python
obj.attr # Get an attribute
obj.attr=value # Set an attribute
del obj.attr # Delete an attribute
```

一旦实例被程序创建,那么对于实例的属性可以自由的添加和删除.对实例属性的操作,存在如下的几个属性访问函数,

| 函数                      | 作用                      |
| ------------------------- | ------------------------- |
| getattr(obj,'name')       | obj.name                  |
| setattr(obj,'name',value) | obj.name=value            |
| delattr(obj,'name')       | del obj.name              |
| hasattr(obj,'name')       | Tests if attribute exists |

这里我们需要注意的是getattr()具有一个比较常用的默认参数值,

```python
x=getattr(obj,'x',None)
```

如果属性不存在,返回的默认值.如果不提供且属性不存在,会抛出AttributeError.

前面我们提到了实例的属性不止有数据还有方法,因此我们需要简要介绍一下实例方法的调用.方法的调用其实是分为两步的,第一步需要先通过.操作符查找到实例的方法对象,第二步则是通过()操作符来调用方法.

```python
s=Stock('ACME',50,91.1)
c=s.cost # 查找并返回方法对象
print(c()) # 调用方法
```

当我们通过一个实例访问他的方法,例如obj.method,即使尚未调用,这个方法已经是一个bound method了,因为他已经绑定了该实例作为self.bound method只出现在实例访问方法,如果是通过类名访问的话,那么获得的对象是普通的函数对象,而不是绑定方法.绑定方法可以通过\_\_self\_\_属性来访问绑定的实例对象属性,通过\_\_func\_\_属性来访问绑定方法的函数属性.因此从这两个角度来说,我出门可以得知调用绑定函数的方法其实就是通过上面的属性完成的,

```python
c.__func__(c.__self__)
```


<a id="org751343b"></a>

## Static and Class Method

前面我们提到了类的定义,它包含了类的实例化对象所共同使用的属性定义.只需要在类定义中定义一次,就可以在所有实例中使用,他会在实例创建的时候被调用,从而为实例创建属性.类属性指的是在\_\_init\_\_函数中定义的实例属性以外定义的变量,可以通过类名调用类变量,同时也可以通过实例名调用类变量.这里需要注意的是,类变量是可以被所有的实例调用,并且对于类变量的修改有如下几种情况,

```python
class Dogs:
    species = "Canis familiaris"
    owner=[]
    d1=Dogs()
    d2=Dogs()
    d1.species='Wolf' # 创建同名的实例属性
    print(d1.species) # 返回Wolf
    print(d2.species) # 返回类属性
    print(Dogs.species) # 返回类属性
    Dogs.species='Wolf' # 可以修改类属性
    d1.owner.append("John") # 可变类变量,可以通过实例修改内容并影响所有实例
    print(d1.owner)
    print(d2.owner)
    print(Dogs.owner)
```

在这里我们需要额外补一句,如果类中设置了\_\_str\_\_方法,那么print函数会自动调用类中定义的\_\_str\_\_方法,而如果str方法没有被定义,那么会查找类是否定义了\_\_repr\_\_方法,如果也没有,那么就会返回<\_\_main\_\_.ClassName object>.除了上面提到的一些修改类变量的方法,我们也可以通过类继承的方式来修改类变量.

除了类变量以外,还可以对于类定义类方法.类方法是直接操作类自身,与普通的函数不同的是,类方法需要用@classmethod装饰器定义.

```python
class SomeClass:
    debug=False
    def __init__(self,x):
        self.x=x
        @classmethod
    def yow(cls):
        print('SomeClass.yow',cls)
```

这里和实例方法类似,类方法中类名会以第一个参数的形式传入.类方法的主要作用其实是可以定义一些不同于\_\_init\_\_函数的初始化函数,如

```python
class Date:
    datefmt='{year}-{month}-{day}'
    def __init__(self,year,month,day):
        self.year=year
        self.month=month
        self.day=day
    def __str__(self):
        return self.datefmt.format(year=self.year,month=self.month,day=self.day)
    @classmethod
    def today(cls):
        tm=time.localtime()
        return cls(tm.tm_year,tm.tm_mon,tm.tm_mday)
```

类方法也可以在一些类继承的情况下解决较为复杂的问题.

除了类变量和类方法以外,类的定义域中还可以存在静态方法的定义.静态方法虽然也是类定义的一部分,但是他其实不会对类或实例进行操作.如果在类中定义了两个同名的函数,那么后面定义的函数定义会覆盖先前函数的定义,这是因为类会创建一个临时的命名空间,只能存在一个同名对象,因此同名标识符的后续赋值会覆盖先前绑定的对象.与前面提到的实例方法和类方法不同的是,静态方法不存在暗含的self(实例)和cls(类)参数.

```python
class SomeClass:
    debug=False
    def __init__(self,x):
        self.x=x
        @staticmethod
    def yowv1():
        print('SomeClass.yow')
```

静态方法的核心价值是命名空间组织和逻辑分组.适用于无状态的辅助函数,与类职责相关但不依赖实例或类的状态.使用静态方法可以提升代码可读性以及模块的内聚性.如果函数不需要考虑实例或类的状态,那么可以定义为静态方法;如果函数未来需要访问类的状态或者支持类继承,那么需要定义为类方法.

综上,类变量通常用于保存全局参数,这个参数在所有实例之间共享.子类继承基类后可以重写相关类变量从而改变类方法行为.类方法最常用是实现备用构造函数.我们常见的类方法名需要有from一词,例如

```python
d=dict.fromkeys(['a','b','c'],0)
print(d)
```


<a id="orgdbc1495"></a>

## Class and Encapsulation

类的主要作用是封装数据和对象的内部实现,而同时类也会提供对外的公共接口,用来操纵对象.因此在Python中区分对象内部实现和对外接口十分重要.但是和C/C++通过语法规定强制执行私有/公有,Python的私有封装是通过对属性的命名来约定俗成的指示属性的预期用途.因为Python默认程序员在编程中有义务遵守私有和公有协议,故而并没有做很强制的约束.

用\_引导的属性名表示这个属性是私有变量,但是虽然名义上是私有变量,我们仍然可以调用并修改他.

```python
class Base:
    def __init__(self,name):
        self._name=name
        b=Base('Guido')
        print(b._name)
        b._name='Dave'
        print(b._name)
```

在继承中,子类仍然可以访问父类的私有属性.实际上,\_只不过是一个命名约定,表示他约定这个属性只在内部可用,但是不会阻止外部访问.为了避免出现私有属性被外界随意调用,我们可以使用\_\_来引导变量.他与单下划线引导的变量不同的是,Python会使用名称修饰,因此我们不能通过\_\_name的方式直接调用他,而是需要使用\_cls\_\_name来调用变量.

```python
class Base:
    def __init__(self,name):
        self.__name=name
        b=Base('Guido')
        print(b._Base__name) # 'Guido'
        b._name='Dave'
        print(b._name) # 'Dave'
```

上面我们调用\_name变量能够返回一个变量,其实是因为在上面的赋值语句中,在实例中创建了一个\_name变量.所以就算用子类继承父类,也不能利用\_\_name来调用修改变量,如果一定要修改也只能使用\_Parent\_\_name的形式.

对于某些需要考虑变量类型的情况下,我们需要使用引入访问器方法,在私有属性上加上get/set函数,但是不幸的是会破坏已有的代码.

```python
class Stock:
    def __init__(self, name, shares, price):
        self.name = name
        self.set_shares(shares)
        self.price = price
    def get_shares(self):
        return self._shares
    def set_shares(self, value):
        if not isinstance(value, int):
            raise TypeError('Expected an int')
        self._shares = value
```

我们希望可以加上类型判断后,并不会影响代码结构,因此引入了property装饰器.

```python
class Stock:
    def __init__(self, name, shares, price):
        self.name = name
        self.shares=shares
        self.price = price
        @property
    def shares(self):
        return self._shares
    @shares.setter
    def shares(self,value):
        if isinstance(value,int):
            self._shares=value
        else:
            raise TypeError('Expected int')
```

我们普通的访问属性会自动触发调用方法,例如我们访问shares属性,则会自动访问property装饰的shares方法;通过对shares的赋值,则会自动访问shares.setter装饰的shares初始化方法.所以我们可以知道property装饰器,其实可以把函数也给装饰成普通变量属性的形式,也就是

```python
class Stock:
    @property
    def cost(self):
        return self.price*self.shares
```

如果我们正在创建对象并且希望对象的各个属性具有一致的接口.

对于\_\_slots\_\_属性的使用,应该保持谨慎态度,虽然他能够减少内存消耗,但是他在继承上可能会有十分复杂的情况,如果一定要使用,建议用在简单的数据结构类中.


<a id="orgba09807"></a>

## Inheritance

继承可以认为是为了扩展现有的对象的方式.我们一般称新类为派生类或子类;父类为基类或超类,父类一般是通过子类后面的括号指定.

```python
class Parents:
    pass
class Child(Parents):
    pass
```

继承一般有两个作用,一是向已有代码中添加新的方法,二则是重写父类方法.如果在子类中重写父类方法时需要使用父类方法,那么我们需要利用super()来调用子类的父类.使用子类继承的时候,我们必须先对父类进行初始化.类的继承其实建立了一个类型关系,我们可以通过isinstance来判断相应的关系,我们可以认为继承定义的子类对象其实是父类对象的一个特殊版本.其实Python提供了object类,可以认为Python的任意对象都是object的子类.不止于单继承,我们可以提供多个父类,从而实现多重继承的子类,其会继承多个父类的特性,但是多重继承由于MRO的存在,需要谨慎使用.综上,继承可用做代码的自定义/可扩展特性,向现有代码添加内容,执行自定义处理.


<a id="org0f760cd"></a>

## Special Method

类通过修改或自定义特殊方法的方式,来定义对象的几乎全部行为.对象有两种字符串模式:str函数会返回适合打印的字符串文本;repr函数会返回具备编程开发信息的字符串文本.repr函数返回的是一个字符串,其可以通过eval函数重新创建一个相应的地政对象.若不存在,这样的字符串则以尽可能易读的形式表示字符串.

实例的创建实际上是分成两步:

1.  先创建一个未初始化的类实例对象

    ```python
    d=Date.__new__(Date)
    ```

2.  再调用初始化函数对类实例对象做初始化操作

    ```python
    d.__init__(2026,2,3)
    ```

因此我们可以通过调用类的\_\_new\_\_方法来自定义一些跳过初始化的创建函数,代码如下所示

```python
import time
class Date:
    @classmethod
    def today(cls):
        tm=time.localtime()
        self=cls.__new__(cls)
        self.year=tm.tm_year
        self.month=tm.tm_mon
        self.day=tm.tm_mday
        return self
```

我们首先需要表明的是,在程序中随意修改类的\_\_new\_\_方法并不被提倡,但我们会在后续中提及某些场景下修改\_\_new\_\_方法的情况.在此我们先介绍一下,\_\_new\_\_方法在类中是以静态方法的形式出现的.这是因为new方法先于实例创建而存在,因此他并不能是实例方法,而new方法不被定义为类方法的原因是,如果是类方法,那么Python就会自动将调用他的类作为第一个参数绑定进入,这可能会影响代码的灵活性,而staticmethod则可以显式的传入一个类对象参数,方便开发者自由决定.

我们继续更详细的介绍new方法的相关用法.

```python
class Dog():
    def __new__(cls, *args, **kwargs):
        print("run the new of dog")
        return super().__new__(cls) 
    def __init__(self):
        print("run the init of dog")
        print(self)
        print(self.__class__)
        a = Dog()
```

上述代码的运行流程是,先查找Dog中的new方法,如果没有找到那就会进一步查找父类的new方法,一直查找到object的new方法.上面的代码中我们查找到Dog中的new方法,其中他会调用super().\_\_new\_\_(cls),也就是调用父类的new方法来创建cls类.这里我们需要注意的是,父类的new方法是可以创建子类实例的,这其实可以认为子类是父类的一种特例.调用父类的new方法中我们可以发现他其实是显式调用了cls类本身,而在init方法中则是显式调用了self实例对象本身.因此new和init还有一个更为重要的区别是,new方法必须要返回一个类对象实例,而init方法则可以没有返回值.

\_\_new\_\_(cls[,&#x2026;])是对象实例化的时候,所调用的第一个方法,他会返回一个未初始化的类对象实例.而init方法则是用于初始化实例,因此在调用init方法之前,必须要调用new方法.new方法的语法结构如下所示,

```python
__new__(cls[,*args,**kwargs])
```

这表明\_\_new\_\_方法的参数至少要有一个类参数,代表实例化的类.这个参数在实例化由Python解释器提供或用户自行显式提供,而后面的参数则会直接传递给init函数.new方法对当前类做实例化,并将实例返回,传给init函数的self,但new方法不代表会自动调用init,只有返回当前类的实例才会调用当前类的初始化.

```python
class A(object):
    def __init__(self, *args, **kwargs):
        print("run the init of A")
    def __new__(cls, *args, **kwargs):
        print("run thr new of A")
        return object.__new__(B, *args, **kwargs)
class B(object):
    def __init__(self):
        print("run the init of B")
    def __new__(cls, *args, **kwargs):
        print("run the new of B")
        return object.__new__(cls)
    a = A()
    print(type(a))
    b = B()
    print(type(b))
```

这个代码运行的结果是a不会调用类A的初始化,因为a实际上是B类实例,并不会调用类A的初始化函数.其实不仅如此,哪怕创建的实例是父类的实例,也是不会调用初始化函数的,如下所示

```python
class Parent:
    def __init__(self):
        print("Parent.__init__ called")
    def __new__(cls, *args, **kwargs):
        print(f"Parent.__new__ called for {cls}")
        return super().__new__(cls)
class Child(Parent):
    def __init__(self):
        print("Child.__init__ called")
    def __new__(cls, *args, **kwargs):
        print("Child.__new__: returning Parent instance!")
        return super().__new__(Child, *args, **kwargs)
    c = Child()
    print("type(c):", type(c))
```

这里的结果其实也是子类不会自动调用初始化方法,因为他生成的是父类实例,而非子类.

我们一般不会修改new方法,但是如果我们希望继承一些不可变的数据类时(如int,str,tuple),修改new方法可以提供一个自定义这些类的实例化过程的途径.我们罗列一些需要修改new方法的场景以及相应实现.

1.  实现单例模式

    ```python
    class Single:
       __instance=None
       @staticmethod
       def __new__(cls,name,age):
           if not cls.__instance:
              cls.__instance=super().__new__(cls)
           return cls.__instance
       def __init__(self,name,age):
          self.name=name
          self.age=age
          a=Single('James',41)
          b=Single('Hinton',36)
          print(id(a)==id(b)) # True 	   
    ```

虽然他只有一个实例,但是我们发现其实他是经过了两次初始化,为了避免初始化的覆盖问题,我们可以进一步加上一个flag来标注只允许一次初始化.

```python
class Single:
   __instance=None
   __first_init=False
   @staticmethod
   def __new__(cls,name,age):
       if not cls.__instance:
          cls.__instance=super().__new__(cls)
       return cls.__instance
   def __init__(self,name,age):
      if not self.__first_init:
         self.name=name
         self.age=age
         self.__first_init=True
             a=Single('James',41)
             b=Single('Hinton',36)
             print(id(a)==id(b)) # True 	   
```

这里面我们其实可以发现一个十分有趣的现象,就是我们直接用了self.\_\_instance来调用相应的属性,而我们在前面提到过这样的属性名会做一个名称修饰,从而导致真实的变量名应该是\_class\_\_instance.这是因为这个过程其实是在编译过程中完成的名称修饰,而这些调用本身都是在类定义内部,所以在做编译的时候会整体上的做名称修饰,故而可以直接形式上的调用.

1.  不可变类型子类化(如int,str,tuple)

    ```python
    class PositiveInt(int):
        def __new__(cls,value):
            if value<0:
                value=0
            return super().__new__(cls,value)
    class UpperStr(str):
        def __new__(cls, content):
            return super().__new__(cls, content.upper())
        x=PositiveInt(-5)
        print(x)
        s = UpperStr("hello")
        print(s)  # "HELLO"
    ```

2.  自定义实例创建逻辑(如对象池,类型转换等)

    ```python
    class Shape:
        def __new__(cls,shape_type,*args):
            if shape_type=='circle':
                return super().__new__(Circle)
            elif shape_type=='square':
                return super().__new__(Square)
            return super().__new__(cls)
    class Circle(Shape): pass
    class Square(Shape): pass
    obj = Shape("circle")
    print(type(obj))
    ```

3.  控制实例数量(对象池)

    ```python
    class LimitedInstances:
        _pool = []
        _max = 3
    
        def __new__(cls):
            if len(cls._pool) < cls._max:
                instance = super().__new__(cls)
                cls._pool.append(instance)
                return instance
             return cls._pool[len(cls._pool) % cls._max]
         a=LimitedInstances()
         b=LimitedInstances()
         print(type(a))
    ```

Python中除了new方法的创建类实例以外,也有\_\_del\_\_方法,其是类对象的一个析构函数.但一般来说他不会调用,当且仅当类对象的引用数为0,也就是程序中用不到这样的类对象的时候才会触发.因此我们需要把他和del操作符区分开,

```python
class Test:
    def __del__(self):
        print('删除引用')
        t=Test() # refcount=1
        c=t # refcount=2
        del t # refcount=1
        del c # refcount=0, 调用__del__函数
```

我们用一些代码简要介绍一下del方法的用法,因为我们修改del函数的情况非常之少,所以我们会在后面简要提及.

```python
class Person(object):
    def __init__(self,name):
        self.name = name
    def __del__(self):
        print("实例对象:%s"%self.name,id(self))
        print("python解释器开始回收%s对象了" % self.name)
        print("类对象",id(Person))
        zhangsan  = Person("张三")
        print("实例对象张三:",id(zhangsan))
        print("------------")
        lisi  = Person("李四")
        print("实例对象李四:",id(lisi))
```

这里我们虽然没有对实例进行删除操作,但是由于在程序结束的时候会自动释放所有程序的占用内存,故而会在程序最后调用del方法.

```python
import time
class Animal(object):
    def __init__(self, name):
        print('__init__方法被调用')
        self.__name = name
    def __del__(self):
        print("__del__方法被调用")
        print("%s对象马上被干掉了..."%self.__name)
        dog = Animal("Dogs")
        del dog
        cat = Animal("Cats")
        cat2 = cat
        cat3 = cat
        print("---马上 删除cat对象")
        del cat
        print("---马上 删除cat2对象")
        del cat2
        print("---马上 删除cat3对象")
        del cat3
        print("程序2秒钟后结束")
        time.sleep(2)
```

上面的程序中的dog对象因为他只有一个引用数,故而在删除自身后会直接调用del方法,但是由于cat对象做了两次赋值,因此其引用数变成了3,我们需要逐步删除已有的引用,最后才会调用del方法.

```python
import sys
class Test:
    pass
t=Test()
print(sys.getrefcount(t))
c=t
print(sys.getrefcount(t))
del c
print(sys.getrefcount(t))
del t
```

Python的sys模块中提供了一个可以读取对象引用数的函数,但值得注意的是,他的引用数读取实际上是比实际的引用数大1的,这是因为测试这个对象引用数的函数本身其实就是对象的一个引用.del方法的危险在于他的调用时机不确定,执行环境不完整,异常不可控,用它去做必须释放的资源在Python中是一个设计错误.因为del依赖的是垃圾回收机制,而不是作用域结束,如果出现了引用环,如

```python
a = BadExample()
a.self = a   # 引用环
```

这样就算我们del a,他的引用数还是1,不会调用del方法.

为了避免出现上面的这个情况,Python引入了弱引用的概念.弱引用表示引用某个对象但是不会增加相应的引用计数.Python提供了weakref模块来实现相应的功能,他可以用于处理复杂的对象关系和内存管理问题的内存泄露问题.但由于他的使用可能十分复杂,因此我们并不推荐经常使用这个模块.

```python
class Node:
    def __init__(self,value):
        self.value=value
        self.prev=None
        self.next=None
        a=Node(1)
        b=Node(2)
        a.next=b
        b.prev=a
        del a
        del b
```

这里我们即使删除了a,b,内存中仍然还是会保留对象a和b的内存占用,这是因为他们存在一个互相引用的现象.Python的变量和C/C++不同,Python的变量并没有绑定内存,而只是一个引用副本,故而释放引用副本并不会影响内存,所以即使我们释放了a的引用,其实a引用的内存仍然存在.弱引用的作用就是打破这个引用循环使部分引用不增加引用计数,让对象能在无强引用时立即被回收.我们在此介绍一些典型场景和代码实例:

1.  观察者模式是一种行为型设计模式,它定义了一种一对多的依赖关系,当一个对象的状态发生改变时,其所有依赖者都会收到通知并自动更新.

    ```python
    mport weakref
    class Subject:
        def __init__(self):
            self._observers=[] # 存储弱存储
        def attach(self,observer):
            self._observers.append(weakref.ref(observer))
        def notify(self):
            # 清理已死亡的对象
            alive=[]
            for ref in self._observers:
                obs=ref()
                if obs is not None:
                    obs.update()
                    alive.append(ref)
                    self.observers=alive
    class Observer:
        def __init__(self,name):
            self.name=name
        def update(self):
            print(f"{self.name} received update")
                    subject = Subject()
                    obs1 = Observer("A")
                    obs2 = Observer("B")
                    subject.attach(obs1)
                    subject.attach(obs2)
                    subject.notify()  # A, B 收到通知
                    del obs1  # obs1 被回收
                    subject.notify()  # 仅 B 收到通知，obs1 自动清理
    ```

这里使用弱引用的优势在于Subject不会阻止Observer被回收,从而避免观察者泄露.

1.  缓存(Cache)避免缓存本身成为内存泄露源.

    ```python
    import weakref
    class WeakCache:
        def __init__(self):
            # key → weakref to value
            # 当 value 无其他强引用时自动消失
            self._cache=weakref.WeakValueDictionary()
        def get(self,key):
            return self._cache.get(key)
        def set(self,key,value):
            self._cache[key]=value
    class A:
        pass
    cache=WeakCache()
    obj=A()
    cache.set("key1",obj)
    print(cache.get("key1"))
    del obj
    print(cache.get("key1"))
    ```

他的优势是缓存不会延长对象生命周期,适合"透明缓存"场景.其中的weakref.WeakValueDictionary,表示字典的值为弱引用.

1.  树/图结构中的父-子反向引用

    ```python
    import weakref
    class TreeNode:
        def __init__(self, value, parent=None):
            self.value = value
            self.parent = weakref.ref(parent) if parent else None  # 弱引用
            self.children = []
        def add_child(self, child):
            child.parent = weakref.ref(self)  # 子→父为弱引用
            self.children.append(child)
    # 使用
    root = TreeNode("root")
    child = TreeNode("child", parent=root)
    root.add_child(child)
    del root  # root 可被回收（child.parent 是弱引用，不阻止回收）
    # child 仍存活（有局部变量引用）
    ```

其优势为子节点持有父节点的弱引用,避免父子互相强引用形成循环.

上面我们提到了del方法存在一些缺点,所以对于某些必须被释放的资源,我们选择使用with语句来取代del方法.with语句的结构如下所示:

```python
with obj as val: # val=obj.__enter__()
    statements
    statements
    # obj.__exit__(ty,val,tb)
```

这里我们可以自定义修改obj的entry/exit方法.给出如下的代码示例,

```python
class Manager:
    def __enter__(self):
        print('Entering')
        return self
    def __exit__(self,ty,val,tb):
        print('Leaving')
        if ty:
            print('An exception occurred')
m=Manager()
with m:
    print("Hello World!")
```

注意,ty,val,tb这三个参数包含尚未处理的异常信息(如果有的话).


<a id="orgb03b918"></a>

## Abstract Base Class

面向对象编程的重要特点就是在于代码复用和代码可拓展.类通常可以被认为是一种设计规范或编程接口.

```python
class IStream:
    def read(self, maxbytes=None):
        raise NotImplementedError()
    def write(self, data):
        raise NotImplementedError()
```

此类一般不会直接实例化,而是作为其他对象的基类.因此我们可以将接口定义为抽象基类(Abstract Base Class,ABC),其中抽象基类的一些实现需要从Python的abc模块中继承,如下所示

```python
from abc import ABC,abstractmethod
class IStream(ABC):
    @abstractmethod
    def read(self,maxtypes=None):
        pass
    @abstractmethod
    def write(self,data):
        pass
```

抽象基类是不能够实例化的,因为他其实只是提供了一些方法的占用,需要在继承中重定义方法实现.除非所有抽象方法都被完整的实现,不然是无法实例化类对象.这其实是可以帮助开发者捕获因疏忽带来的编程错误.不仅如此,传统角度来说,我们如果希望判别对象是否为我们期待的接口,需要手动逐个检查验证方法是否存在且是否可调用,

```python
def write_data(data, stream):
    if not (hasattr(stream, 'read') and callable(stream.read) and
            hasattr(stream, 'write') and callable(stream.write)):
        raise TypeError('Expected a Stream with read() and write() methods')
    ...
#+END_SR
这一流程十分复杂且极其容易遗漏,而抽象基类则可以十分方便的简化上述的类型检测,如下所示
#+BEGIN_SRC python
def write_data(data,stream):
    if not isinstance(stream,IStream):
        raise TypeError('Expected a Stream with read() and write() methods')
```

在抽象基类中,存在一种比较常见的用法就是处理器类.我们有些时候会在代码中实现一些通用算法,然后将一些关键或可拓展的步骤委托给外部提供的处理器对象.这个方式其实就是策略设计模式.策略设计模式表示在程序中定义了一系列算法或策略,并将每个算法封装在独立的类中,使得它们可以互相替换.通过使用策略模式,可以在代码运行时根据需要选择不同的算法封装对象,而不需要修改客户端代码.他的优点是降低了算法类的职责,使各个算法可以独立变化并相互替换.而且使得增加新算法十分容易,降低对原有系统的侵入,从而使得程序可扩展可维护性增强.但是缺点就是程序功能不断丰富的过程中,程序从局部来看变的更复杂了.

我们给出一个简单的处理器类的代码示例

```python
def print_table(records,fields,formatter):
    formatter.headings(fields)
    for r in records:
        rowdata=[getattr(r,fieldname,'undef') for fieldname in fields]
        formatter.row(rowdata)
```

上面的代码中formatter其实就是一个处理器类,他在print\_table里面被不断调用,因此使用处理器类的关键在于算法的关键步骤委托给独立的处理器类,从而实现代码的解耦.处理器类和抽象基类一样,都是具有自己的类定义,一般来说他只需要包含需要实现或者自定义的方法.处理器类在Python标准库中极为常见,他的优势是提供了代码的灵活性;处理器类和代码实现解耦;处理器类在其他的代码上下文中可复用.

抽象基类的另一个特例在于构造模板类.模板类实现通用算法,但是将某些特殊化步骤委托给子类实现.如

```python
class CSVParser:
    def parse(self, filename):
        records = []
        with open(filename) as f:
            rows = csv.reader(f)
            self.headers = next(rows)
            for row in rows:
                record = self.make_record(row)  # 需子类实现的步骤
                records.append(record)
        return records
    def make_record(self, row):
        raise RuntimeError('Must implement')  # 未实现时抛出错误
```

这种类是无法直接是用的,必须通过子类继承来补充缺失的功能.如下所示

```python
class DictCSVParser(CSVParser):
    def make_record(self, row):
        return dict(zip(self.headers, row))
parser = DictCSVParser()
portfolio = parser.parse('portfolio.csv')
```

他的核心思想是用户仅需定义小型子类提供缺失部分,大部分功能由基类提供.但实际上,上面的这个结构通过模板类和子类的结构从代码角度来看其实十分复杂,其实可以直接用函数回调的方式直接替代.

```python
def parse_csv(filename, make_record):
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headers = next(rows)
        for row in rows:
            record = make_record(headers, row)  # 用户传入回调函数
            records.append(record)
    return records
def make_record(headers, row):  # 用户实现
    ...
```

因为模板模式可能会过于复杂,而函数的回调会更加简洁.


<a id="orgeed8e3f"></a>

## Advanced Inheritance

继承是代码复用(定制与扩展)的工具,子类可以对父类已有的方法进行自定义修改与扩展.多重继承会使得子类继承所有父类的特性.Python允许协作式多重继承,子类可以显式安排多个父类协作.子类定义时父类的顺序十分重要,他会直接影响父类在方法解释顺序也就是MRO中的顺序.调用子类属性的时候,会在他的MRO中寻找相应的属性.此外,super()函数会按照MRO依次调用父类的方法,形成协作,这里需要注意的是super()不一定是父类,而是MRO的下一个类.例如,

```python
from abc import ABC,abstractmethod
class TableFormatter(ABC):
    @abstractmethod
    def headings(self,headers):
        raise NotImplementedError()
    @abstractmethod
    def row(self,rowdata):
        raise NotImplementedError()
class TextTableFormatter(TableFormatter):
    def headings(self,headers):
        print(' '.join('%10s' % h for h in headers))
        print(('-'*10+' ')*len(headers))
    def row(self,rowdata):
        print(' '.join('%10s' % d for d in rowdata))
class UpperHeadersMixin:
    def headings(self,headers):
        super().headings([h.upper() for h in headers])
class UpperHeadersFormatter(UpperHeadersMixin,TextTableFormatter):
    pass
```

这里的UpperHeadersMixin类的heading方法调用了super方法,他其实并不一定代表UpperHeadersMixin的父类,因为我们会在UpperHeadersFormatter里调用,所以他其实是表示在MRO顺序下往后的某一个类,未必是他自己的父类. Mixin是专门向其他类定义添加额外功能而设计的类.其核心思想是用户实现基础功能后,Mixin可自动补充额外的函数功能.他的主要作用是可以减少代码重复,减少需要编写的代码量.他的典型用途是为基本对象添加可选功能(如线程支持,持久化等),用户通过组合不同部件装配所需对象.
