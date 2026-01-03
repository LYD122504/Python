import stock
# Exercise Representation of Instances
goog=stock.stock('GOOG',100,190.10)
ibm=stock.stock('IBM',50,91.23)
print(goog.__dict__)
print(ibm.__dict__)

# Exercise 5.2 Modification of Instance Data
goog.date='6/11/2007'
print(goog.__dict__)
print(ibm.__dict__)
goog.__dict__['time']='9.45am'
print(goog.time)

# Exercise 5.3 The role of classes
print(goog.__class__)
print(ibm.__class__)
print(goog.cost())
print(ibm.cost())
print(stock.stock.__dict__)
print(stock.stock.__dict__['cost'])
print(stock.stock.__dict__['cost'](goog))
print(stock.stock.__dict__['cost'](ibm))
stock.stock.foo=42
print(goog.foo)
print(ibm.foo)
class Foo(object):
    a=13
    def __init__(self,b):
        self.b=b
f=Foo(10)
g=Foo(20)
print(f.a,g.a,sep=',')
print(f.b,g.b,sep=',')
Foo.a=42
print(f.a,g.a,sep=',')

# Exercise 5.4 Bound Methods
s=goog.sell
print(s)
print(s(25))
print(goog.shares)
"""
访问该绑定方法背后对应的原始函数对象
m.__func__   # 原始函数对象
m.__self__   # 绑定的实例
bound_method.__func__ 等价于定义在类中的函数对象本身
"""
print(s.__func__)
print(stock.stock.__dict__['sell'])
print(s.__self__)
# 调用函数所有部分会整合在一起
s.__func__(s.__self__,25)
print(goog.shares)

# Exercise 5.5 Inheritance
class NewStock(stock.stock):
    def yow(self):
        print('Yow!')

n=NewStock('ACME',50,123.45)
print(n.cost())
n.yow()
print(NewStock.__bases__)
print(NewStock.__mro__)
for cls in n.__class__.__mro__:
    if 'cost' in cls.__dict__:
        break
print(cls)
print(cls.__dict__['cost'])