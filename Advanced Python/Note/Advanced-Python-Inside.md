---
title: Advanced Python-Inside Python Objects
date: 2026-02-10 15:05:42
tags:
    - Python
categories: Advanced Python
mathjax: true
---

# Inside Python Objects


<a id="org96f57f2"></a>

## Underlying dictionary

字典是命名化值的集合,用户自定义的对象的底层使用字典,如实例数据和类成员.换言之,整个对象系统的底层是基于字典.实例的\_\_dict\_\_字典属性会用于存储实例数据,在创建实例属性并赋值的时候,实际上就是对\_\_dict\_\_字典的元素填充.并且不同实例的\_\_dict\_\_字典属性是私用的,并不会互通共享.换言之,其实就是如果程序中创建了100个实例,那么也会有100个不同的实例字典.与实例的\_\_dict\_\_字典不同的是,类也是存在\_\_dict\_\_字典属性的,其是用于存储类成员.类和对象在逻辑上是具有很强的联系的,也就是实例是类的可操作对象,类提供了实例的数据属性和操作行为.实例的\_\_class\_\_属性返回的是其实例化的类,因此可以从实例反连接到类.

<!--more-->

```python
class Stock:
    def __init__(self,name,shares,price):
        self.name=name
        self.shares=shares
        self.price=price
    def cost(self):
        return self.price*self.shares
    def sell(self,nshares):
        self.shares-=nshares
print(Stock.__dict__)
s=Stock('GOOG',100,490.10)
print(s.__dict__)
print(s.__class__)
```

实例字典是私有的,而类字典则是所有实例都可以共享.

Python通过.操作符来实现对属性的调用,如下所示

```python
x=obj.name # Getting
obj.name=value # Setting
del obj.name # Deleting
```

这些操作其实可以直接反映到底层字典,因此修改和删除实例数据会直接在底层字典上更新.如果我们希望读取实例的某个属性,程序会优先在局部实例字典中查找,如果没有,再查找类字典.这种查找方式会使类成员被所有实例共享.


<a id="orgcc766f3"></a>

## Inheritance

继承在前面已经提到了很多次,这里主要是介绍一下关于多重继承的继承结构和方法调用上.Python允许类从多个父类中继承,其相关的直接父类会以元组的形式存储在每个类的\_\_bases\_\_属性中,但对于父类的父类并不会存储返回.而在类属性中,还有一个类似的属性\_\_base\_\_,他会返回第一个直接父类,一般用于单继承.\_\_bases\_\_属性会提供指向父类的链接,从而可以扩展用于查找属性的搜索过程.因此完整的搜索链其实是先查找局部实例字典,再查找类字典,最后查找父类字典.

在继承层次结构上,属性是通过沿着继承树查找.若只是单继承,则查找线路只有一个直线,程序会在第一个匹配的对象时停止并返回.

```python
class A(object): pass
class B(A): pass
class C(A): pass
class D(B): pass
class E(D): pass
print(E.__mro__)
```

这种继承链会在类完成继承的时候预计算,并且存储在类的\_\_mro\_\_属性.多继承的MRO会比较复杂,但是我们在前面已经提到了相关的算法,如感兴趣可以查阅.

```python
class A(object): pass
class B(object): pass
class C(A,B): pass
class D(B): pass
class E(C,D): pass
print(E.__mro__)
```

在类方法的重写中,如果我们需要调用父类的方法,当然可以直接明确的指出所使用的父类名称,如

```python
class Base:
    def spam(self,x):
        print(f"Base.spam({x})")
class A(Base):
    def spam(self,x):
        print(f"A.spam({x})")
        Base.spam(x)
```

这样会很明确,但是如果继承结构的变化会使得程序的修改和维护变得困难.因此为了重写方法,我们一般选择使用super()函数.super()函数会调用给MRO上的下一个匹配的类,而不是直接父类,因此在不同的MRO中,同一个类的super()返回的可能不是同一个类,这里我们需要额外注意.

我们简要介绍一下继承设计的几个原则:第一,需要有兼容的方法参数,重写方法在整个继承结构中必须存在兼容参数..如果方法参数各不相同,那么可以使用关键字参数.代码如下所示

```python
class Base:
    def spam(self,x):
        print(f"Base.spam({x})")
class A(Base):
    def spam(self,x):
        print(f"A.spam({x})")
        super().spam(x)
class B(Base):
    def spam(self, x, y):
        print(f"B.spam({x}, {y})")
        super().spam(x)
class C(A, B):
    def spam(self, x, y):
        print(f"C.spam({x}, {y})")
        super().spam(x, y)
try:
    c = C()
    c.spam(1, 2)
except TypeError as e:
    print(f"错误: {e}\n")
```

这里会因为类C调用类A的spam函数,并且传入两个参数,这与类A的spam函数的所需参数不同,因此会报错.故而需要采用关键字参数,如下所示,

```python
class BaseFixed:
    def spam(self, x, **kwargs):
        print(f"BaseFixed.spam(x={x})")
        # 消耗掉已处理的参数，传递剩余参数
        kwargs.pop('extra', None)  # 可选：清理特定参数
class AFixed(BaseFixed):
    def spam(self, x, **kwargs):
        print(f"AFixed.spam(x={x})")
        super().spam(x, **kwargs)  # 安全传递所有未使用参数
class BFixed(BaseFixed):
    def spam(self, x, y, **kwargs):  # 可安全添加新参数
        print(f"BFixed.spam(x={x}, y={y})")
        super().spam(x, **kwargs)
class CFixed(AFixed, BFixed):
    def spam(self, x, y, z=None, **kwargs):
        print(f"CFixed.spam(x={x}, y={y}, z={z})")
        super().spam(x, y=y, z=z, **kwargs)
# 测试：MRO 顺序为 CFixed -> AFixed -> BFixed -> BaseFixed -> object
print("MRO:", [cls.__name__ for cls in CFixed.__mro__])
print()
c_fixed = CFixed()
c_fixed.spam(1, y=2, z=3)
```

关键字参数的存在可以安全的传递一些额外的参数.第二,方法链必须要终止,super()函数不可以永远调用,因为MRO的长度是有限的;第三,在任何地方都可以使用super()函数.


<a id="orge4b006e"></a>

## Descriptor

描述符是Python最强大但常被忽略的元编程工具,其用于实现property,classmethod等高级特性的底层实现.描述符指的是实现了描述符协议(<span class="underline"><span class="underline">get</span></span>,\_\_set\_\_,\_\_delete\_\_中至少一个)的类实例.若类试图访问类中的某个属性,我们会检测其是否具有描述器符特征,如果有,那么他的相关调用就会被描述符覆盖.

```python
class Descriptor:
    def __init__(self,name):
        self.name=name
    def __get__(self,instance,owner):
        return instance.__dict__[self.name]
    def __set__(self,instance,value):
        instance.__dict__[self.name]=value
    def __delete__(self,instance):
        pass
class Foo:
    a=Descriptor('a')
```

从上面的代码来看,我们发现描述符的实例其实是类属性,但是他其实操作的是实例字典,也就是他会拦截实例属性的访问行为.

Python属性访问遵循严格优先级,这是理解描述符的关键:

<img src="https://github.com/LYD122504/picx-images-hosting/raw/master/20260210/2026-02-09_11-04-34_screenshot.icn4ugmr5.png" style="zoom:50%;" />

 数据描述符指的是实现了\_\_set\_\_或\_\_delete\_\_的描述符类,他会拦截赋值写入;非数据描述符指的则是只实现了\_\_get\_\_方法,他不会拦截对实例字典的访问,相反他会被实例字典覆盖.查找的路线是数据描述符,实例字典,非数据描述符,类字典.给出如下的代码实例

```python
class DataDesc:
    def __get__(self, instance, owner):
        print(f'__get__: {instance=}, {owner=}')
        return instance.__dict__.get('attr', 'default')    
    def __set__(self, instance, value):
        print(f'__set__: {value=}')
        instance.__dict__['attr'] = value
class A:
    attr = DataDesc()  # 数据描述符（有 __set__）
a = A()
a.attr = 42          # → __set__: value=42（被拦截）
print(a.attr)        # → __get__: instance=<A...>, owner=<class 'A'> → 42
print(a.__dict__)    # → {'attr': 42}
```

上面的a.attr试图访问的是实例字典的属性,但是被数据描述符拦截,从而调用数据描述符的方法.

```python
class NonDataDesc:
    def __get__(self, instance, owner):
        print('__get__ called')
        return 'from descriptor'
class B:
    attr = NonDataDesc()  # 非数据描述符（无 __set__）
b = B()
print(b.attr)
b.attr = 'instance value'  # 直接写入实例字典，不触发 __set__
print(b.attr)              # → 'instance value'（实例字典优先）
print(B.attr)              # → __get__ called → 'from descriptor'
```

这里我们先调用b.attr时,发现他会调用非数据描述符的get方法,如果我们对b.attr赋值以后,那么他的相关调用就会被实例字典覆盖,除非我们用类属性的方式调用,因为非数据描述符本质上是一个类属性.

从上面的代码,我们可以看出描述符其实是包含了实例,类和数值的信息.在程序编写中我们需要注意的是,self是描述符本身,instance则表示是操作的实例对象.虽然他的调用从形式上来看和实例字典是一样的,但是我们可以把他用如下的方式拆解.

```python
q=A.__dict__['attr']
print(q) # <__main__.DataDesc object at 0x00000279B19DA930>
q.__set__(a,43) # __set__: value=43
print(q.__get__(a,a.__class__))
# __get__: instance=<__main__.A object at 0x000001FCD0FDA9F0>, owner=<class '__main__.A'>
# 43
```

我们通过代码实现可以知道,描述符是可以存储和检索数据的,他会直接操作实例底层字典,来实现对数据的读写操作.这也就是我们前面提到的,描述符是一个类属性,但是他的操作对象则是实例对象的底层字典.因此许多重要的类行为都是通过描述符实现的,例如实例方法,静态方法,类方法以及property装饰器,我们在后续会给出一些自定义的实现.我们前面提到过函数的调用是分成两个步骤的,先通过.操作符查找到绑定方法,再用()操作符去调用相关方法.就此我们用描述符的角度去解释一下

```python
import stock
s=stock.Stock('GOOG',100,490.10)
# class attribute lookup
value=stock.Stock.__dict__['cost']
print(value)
#descriptor check
print(hasattr(value,'__get__')) # true
print(hasattr(value,'__set__')) # false
print(hasattr(value,'__delete__')) # false
#invocation
result=value.__get__(s,stock.Stock)
print(result)
print(result())
```

故而可知value其实就是一个非数据描述符,对其进行赋值后,会返回一个绑定方法,但这个其实只是一个返回设定,如果我们自定义了一个返回为字符串,那么就是字符串,只是我们可以通过描述符进一步解释实例方法的调用.因此非数据描述符被激发的前提是在实例字典上没有匹配的属性,他才会被激发.

\_\_slots\_\_和\_\_dict\_\_不同的是他在实例创建之初,就会预先检查类字典中是否有同名属性,如有则报错,若没有,那么就会计算分配一个数组空间.从底层来看,每个slot名都会创建一个描述符用来完成在指定的位置进行简单的读取写入操作.但我们仍然可以自定义一个描述符,但需要注意的是如果我们希望可以实现对slots的描述符,那么类属性和slots必须要分开,不然是无法创建slots数组的,我们给出正确的代码示例.

```python
class Descriptor:
    def __init__(self,name):
        self.name='_'+name
    def __get__(self,instance,cls):
        if instance==None:
            return self
        return getattr(instance,self.name)
    def __set__(self,instance,value):
        setattr(instance,self.name,value)
class A:
    __slots__=('_x','_y')
    x=Descriptor('x')
    y=Descriptor('y')
a=A()
a.x=10
a.y=20
print(a.x)
print(a.y)
```

这里我们不用前面常见的操作底层字典的方式是因为slots并没有像底层字典一样提供存储空间,而是向程序宣告允许的属性名是什么,其相关的内部空间由底层程序控制,因此我们需要调用setattr和getattr等属性访问函数.其次,这里的类A中在类字典中是具有属性x和y的,而对于实例slots的\_x和\_y则是通过调用类属性的数据描述符x和y操作.同样slots也是支持删除操作的,因为slots的主要目的其实是为了内存优化和属性限制,也就是控制某些属性的存在.

描述符的主要作用其实是描述数据,提供比property装饰器更为精细的控制,可以使用更少的重复代码.

```python
import numbers
class Integer:
    def __init__(self,name):
        self.name=name
    def __set__(self,instance,value):
        if not isinstance(value,int):
            raise TypeError('Expected an integer')
        instance.__dict__[self.name]=value
class String:
    def __init__(self,name,maxlen):
        self.name=name
        self.maxlen=maxlen
    def __get__(self,instance,cls):
        return instance.__dict__[self.name]
    def __set__(self,instance,value):
        if not isinstance(value,str):
            raise TypeError('Expected a string')
        if len(value)>self.maxlen:
            raise TypeError('The length must be less than 8')
        instance.__dict__[self.name]=value
class Real:
    def __init__(self,name):
        self.name=name
    def __get__(self,instance,cls):
        return instance.__dict__[self.name]
    def __set__(self,instance,value):
        if not isinstance(value,(int,float)):
            raise TypeError('Expected an integer or float')
        if not isinstance(value,numbers.Real):
            raise TypeError('The number must be real')
        instance.__dict__[self.name]=value
class Stock:
    name=String('name',maxlen=8)
    shares=Integer('shares')
    price=Real('price')
s=Stock()
s.name='Hello'
print(s.name)
```

这里我们可以发现Integer其实没有设置get方法,这是因为Python内部其实也是有get方法的,如果我们在描述符内不去设置get方法,那么程序就会调用程序自带的get方法,这要求我们所调用的名字和实例字典里的名字需要完全一样.

```python
class Integer:
    def __init__(self,name):
        self.name='_'+name
s.shares=1
print(s.shares) # <__main__.Integer object at 0x000002A278692300>
print(s._shares) # 1
```

其实如果我们省略了get方法的话,可以认为就是直接去访问实例字典.get方法可以被两种方式调用,一是通过绑定实例的方式,也就是直接使用实例调用;二则是通过类调用,这样他不会绑定实例.这里我们可以知道上面的描述符对get方法的实现存在一个问题,因为它本质上是一个类方法,但是我们的实现中只考虑实例调用的情况,所以我们需要补充一下get方法,

```python
class Descriptor:
    def __get__(self,instance,cls):
        if instance is None:
            # If no instance given, return the descriptor
            # object itself
            return self
        else:
            # Return the instance value
            return instance.__dict__[self.name]
```

我们在前面中定义描述符的时候,实例属性的名称需要显示给出,但一般而言我们为了方便起见都会定义成原来的名字,如果多次出现,会使得代码十分臃肿.因此Python3.6版本以上提供了名称设置器的方法以简化描述符的实例化.

```python
class Descriptor:
    def __init__(self, name=None):
        self.name = name
    def __get__(self, instance, cls):
        if instance is None:
            return self
        return instance.__dict__[self.name]
    def __set_name__(self, cls, name):
        self.name = name
class Spam(object):
    x=Descriptor() # x.__set_name__(Spam,'x')
```

我们可以让类的多个属性分别绑定在同一个描述符,但是不可以让同一个属性绑定在多个描述符上,如果发生了,那么后定义的会覆盖前定义的.

```python
class Integer:
    def __init__(self, name=None):
        self.storage_name = name if name is None else '_' + name    
    def __set_name__(self, owner, name):
        # Python 3.6+ 自动捕获属性名（推荐）
        if self.storage_name is None:
            self.storage_name = '_' + name  
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.storage_name)
    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError(f"{self.storage_name} must be int")
        setattr(instance, self.storage_name, value)
class Point:
    x = Integer()  # 实例1：管理 x
    y = Integer()  # 实例2：管理 y 
    def __init__(self, x, y):
        self.x = x
        self.y = y
p = Point(10, 20)
print(p.x, p.y)  # 10 20
p.x = 30         # → Integer实例1的__set__
p.y = 40         # → Integer实例2的__set__
print(p.x, p.y)  # 30 40
```

这里x和y是两个独立的Integer实例,并且他们通过\_\_set\_name\_\_方法来获得唯一的实例属性名,他们不会互相干扰,各自管理自己的属性.

我们给出一些描述符的简单实现,覆盖静态方法,类方法,property装饰器等场景.

```python
class Mystatic:
    def __init__(self,func):
        self.func=func
    def __get__(self,instance,owner):
        # 无论是实例访问还是类访问都返回函数
        return self.func
class Math:
    @Mystatic
    def add(x,y):
        return x+y
print(Math.add(1,2))
m=Math()
print(m.add(2,3))
```

这里的特点就是get方法返回的是self.func,并没有和任何类,实例进行绑定.因此对这个方法而言,其实在实现逻辑上并不属于类和实例,只是在编程逻辑上应该属于类.

```python
class Myclass:
    def __init__(self,func):
        self.func=func
    def __get__(self,instance,cls):
        def wrapper(*args,**kwargs):
            return self.func(cls,*args,**kwargs)
        return wrapper
class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
    @Myclass
    def today(cls):
        import datetime
        now = datetime.date.today()
        return cls(now.year, now.month, now.day)
d = Date.today()
print(d.year)     # 2026
```

属性访问Date.today触发描述符协议,调用MyClass.\_\_get\_\_(None,Date),此时get方法会返回一个闭包wrapper,他捕获了owner=Date和原始函数self.func.此时调用Date.today,其实就是调用的就是wrapper函数,只是wrapper函数已经给定了第一个参数为类,所以他其实就是一个类方法.

```python
class Myproperty:
    def __init__(self,fget=None,fset=None,fdel=None,doc=None):
        self.fget=fget # gettr 函数
        self.fset=fset # settr 函数
        self.fdel=fdel # deleter 函数
        self.__doc__=doc or (fget.__doc__ if fget else None)
    def __get__(self,instance,owner):
        if instance is None:
            return self
        if self.fget is None:
            raise AttributeError("unreadable attribute")
        return self.fget(instance)  # 调用 getter
    def __set__(self,instance,value):
        if self.fset is None:
            raise AttributeError
        self.fset(instance,value)
    def __delete__(self,instance):
        if self.deleter is None:
            raise AttributeError
        self.fdel(instance)  # 调用 deleter
    def setter(self, fset):
        return type(self)(self.fget, fset, self.fdel, self.__doc__)
    def deleter(self, fdel):
        return type(self)(self.fget, self.fset, fdel, self.__doc__)
class Circle:
    def __init__(self, radius):
        self._radius = radius    
    @Myproperty
    def radius(self):
        """圆的半径"""
        return self._radius 
    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("半径不能为负")
        self._radius = value   
    @radius.deleter
    def radius(self):
        del self._radius
c = Circle(5)
print(c.radius)    # 5（触发 __get__ → fget）
c.radius = 10      # 触发 __set__ → fset
del c.radius       # 触发 __delete__ → fdel 
```

我们首先用Myproperty装饰器装饰了radius函数,相当于用了如下代码,

```python
radius=Myproperty(radius)
```

此时的radius就是Myproperty的一个实例对象.而后的radius.setter和deleter用来填充需要的其他相关代码.

```python
class CachedProperty:
    def __init__(self,func):
        self.__name__=func.__name__
    def __get__(self,instance,owner):
        if instance is None:
            return self
        print('Called get function')
        value=self.func(instance)
        setattr(instance,self.__name__,value)
        return value
class MyClass:
    def __init__(self,data):
        self._data=data
    @CachedProperty
    def processed_data(self):
        result=[x**2 for x in self._data]
        return result
obj=MyClass([1,2,3,4,5])
print(obj.processed_data)
# Called get function
# [1, 4, 9, 16, 25]
print(obj.processed_data)
# [1, 4, 9, 16, 25]
```

这里我们发现他调用了两次相同的函数,但实际上非数据描述符只调用了一次,因为调用非数据描述符的时候在实例字典中设置了一个同名属性,从而覆盖非数据描述符的调用.


<a id="orgb9447a9"></a>

## Attribute Access Methods

类可以通过实现特定的特殊方法来拦截对属性的访问操作,如获取(get),设置(set)和删除(delete).其中的调用流程大体如下所示,获取流程:我们调用obj.x,在程序内部会先试用obj.\_\_getattribute\_\_('x'),如果程序没有找到相应的属性,则会调用obj.\_\_getattr\_\_('x')作为后备安全方法.设置流程:我们调用obj.x=val,在程序内部会直接调用obj.\_\_setattr\_\_('x',val).删除流程:我们调用del obj.x,在程序内部会直接调用obj.\_\_delattr\_\_('x').

getattribute方法的语法结构如下所示,

```python
__getattribute__(self,name)
```

每次读取属性时都会调用这个方法,无论属性是否存在.他的默认行为是按顺序查找描述符,而后是实例字典,最后则是基类(沿着MRO向上查找).如果上面的查找流程都没有查找的同名属性,那么就会调用\_\_getattr\_\_作为备用函数.

getattr方法的语法结构如下所示,

```python
__getattr__(self,name)
```

他的整个调用方式和上面的getattribute方法一致,他只有在上面的getattribute方法查找不到的时候才会被调用.其默认行为是会抛出异常AttributeError.我们可以自定义修改设置,从而适合实现动态属性,默认值返回,代理转发等功能.

我们用如下的代码解释二者的区别,

```python
class Demo:
    def __init__(self):
        self.existing = 'I exist'
    def __getattribute__(self, name):
        print(f'__getattribute__ 被调用: "{name}"')
        try:
            return super().__getattribute__(name)
        except AttributeError:
            print(f"标准查找失败,需要触发getattr")
            raise
    def __getattr__(self,name):
        print(f"__getattr__ 被调用（后备）: '{name}'")
        return f"默认值: {name}"
obj=Demo()
print("\n--- 访问存在的属性 ---")
print(obj.existing)
print("\n--- 访问不存在的属性 ---")
print(obj.missing)
```

上面我们可以发现,存在的属性会直接调用getattribute方法,并能够查找直接返回值.而缺失的属性则是getattribute方法同样也会被调用,但是他会返回一个异常,同时自动调用getattr方法.所以这两个方法的核心区别是\_\_getattribute\_\_方法的优先级是最高的,只要读取属性就不需要被调用;\_\_getattr\_\_方法仅在属性缺失的时候作为后备被调用.

setattr方法的语法结构如下,

```python
__setattr__(self,name,value)
```

其只在每次对属性赋值的时候才会调用.默认行为是检查是否为数据描述符,如果是,那么就调用内部的set方法,否则,就会在实例字典中存入到相应属性中.delattr方法的语法结构如下,

```python
__delattr__(self,name)
```

其只在属性删除的时候才会被调用.默认行为是检查是否为数据描述符,如果是,那么就会调用内部的delete方法,否则,就会从实例字典中删除属性.上述的类方法都可以通过重定义的方式来自定义属性访问方法,以符合更多的应用场景,如创建包装对象,代理或其他的情况.

代理转发场景

```python
class Proxy:
    def __init__(self,obj):
        self._obj=obj
    def __getattr__(self,name):
        print('getattr: ',name)
        return getattr(self._obj,name)
class Circle:
    def __init__(self,rad):
        self.radius=rad
    def area(self):
        import math
        return math.pi*self.radius**2
c=Circle(4.0)
print(c.radius)
print(c.area())
p=Proxy(c)
print(p)
print(p.radius)
print(p.area())
```

这里的Proxy持有内部对象\_obj,其会用于存储外部的类,从而形成对\_obj的代理访问.所有不存在于Proxy类自身的属性访问都会触发\_\_getatttr\_\_,同时将调用请求转发给内部对象\_obj.适合于实现日志记录,权限控制,远程调用等包装逻辑.

委托模式场景

```python
class A:
    def foo(self):
        print('A.foo')
    def bar(self):
        print('A.bar')
class B:
    def __init__(self):
        self._a=A()
    def bar(self):
        print('B.bar')
        self._a.bar()
    def __getattr__(self,name):
        return getattr(self._a,name)
b=B()
b.foo()# 输出: A.foo(委托给A)
b.bar()  # 输出: B.bar → A.bar(B自定义+委托)
```

委托可以作为继承的一个替代方案,从而实现更为灵活的组合式设计.需要注意的是,\_\_getattr\_\_不会拦截特殊方法,例如\_\_len\_\_,\_\_getitem\_\_等,如果需要支持,必须要显式实现,

```python
class B:
    def __init__(self):
        self._a=A()
    def __getitem__(self,index):
        return self._a[index]
    def __getattr__(self):
        return getattr(self._a),name)
```

<a id="org9881db1"></a>
