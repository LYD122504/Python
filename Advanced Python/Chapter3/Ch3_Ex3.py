import time
import stock
import reader
class SomeClass:
    debug=False
    def __init__(self,x):
        self.x=x
    @classmethod
    def yow(cls):
        print('SomeClass.yow',cls)
    @staticmethod
    def yowv1():
        print('SomeClass.yow')
print(SomeClass.debug)
s=SomeClass(42)
print(s.debug)
print(SomeClass.yowv1())

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
class USDate(Date):
    datefmt='{month}/{day}/{year}'
a=Date(2025,12,31)
print(a)
b=USDate(2025,12,31)
print(b)
c=USDate.today()
print(c)

row=['AA','100','32.20']
s=stock.Stock.from_row(row)
print(s.name)
print(s.shares)
print(s.price)
print(s.cost())
s=stock.DStock.from_row(row)
print(s.name)
print(s.shares)
print(s.price)
print(s.cost())

class Row:
         def __init__(self, route, date, daytype, numrides):
             self.route = route
             self.date = date
             self.daytype = daytype
             self.numrides = numrides
         @classmethod
         def from_row(cls, row):
             return cls(row[0], row[1], row[2], int(row[3]))
s=reader.read_csv_as_instances('../Data/ctabus.csv',Row)
print(len(s))
d=dict.fromkeys(['a','b','c'],0)
print(d)

class Dog:
    species = "Canis familiaris"  # 类变量

d1 = Dog()
d2 = Dog()

d1.species = "Wolf"  # ❌ 实际创建了实例变量 d1.species

print(d1.species)        # 'Wolf'      → 实例变量
print(d2.species)        # 'Canis familiaris' → 类变量
print(Dog.species)       # 'Canis familiaris' → 未被修改

print(d1.__dict__)       # {'species': 'Wolf'}  → 实例有自己的属性
print(d2.__dict__)       # {}                   → 无实例变量，回退到类变量