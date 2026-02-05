class Parent:
    def spam(self):
        print('Parent')
class A(Parent):
    def spam(self):
        print('A')
        super().spam()
class B(Parent):
    def spam(self):
        print('B')
        super().spam()
class Child(A, B):
    pass
c = Child()
c.spam()

class Dog:
    def noise(self): return 'Woof'
    def chase(self): return 'Chasing!'
class Bike:
    def noise(self): return 'On Your Left'
    def pedal(self): return 'Pedaling!'
class Loud:
    def noise(self):
        return super().noise().upper()  # 依赖 super() 链式调用

class LoudDog(Loud, Dog):  # Mixin 在前
    pass

class LoudBike(Loud, Bike):
    pass
d = LoudDog()
print(d.noise())
import stock, reader
portfolio = reader.read_csv_as_instances('../Data/portfolio.csv', stock.Stock)
from tableformat import print_table,create_formatter
formatter = create_formatter('csv', column_formats=['"%s"','%d','%0.2f'])
print_table(portfolio, ['name','shares','price'], formatter)
formatter = create_formatter('text', upper_headers=True)
print_table(portfolio, ['name','shares','price'], formatter)