class Stock:
    def __init__(self,name,shares,price):
        self.name=name
        self.shares=shares
        self.price=price
    
    def cost(self):
        return self.shares*self.price
    
    def sell(self,nshares):
        self.shares-=nshares

# Add a new method
class MyStock(Stock):
    def panic(self):
        self.sell(self.shares)
s=MyStock('GooG',100,490.1)
s.sell(25)
print(s.shares)
s.panic()
print(s.shares)

# Redefine an existing method
class MyStock(Stock):
    def cost(self):
        return 1.25*self.shares*self.price
s=MyStock('GOOG',100,490.10)
print(s.cost())

# Overriding
class MyStock(Stock):
    def cost(self):
        actual_cost=super().cost()
        return 1.25*actual_cost
s=MyStock('GOOG',100,490.10)
print(s.cost())

# __init__ and inheritance
class MyStock(Stock):
    def __init__(self,name,share,price,factor):
        super().__init__(name,share,price)
        self.factor=factor
    def cost(self):
        return self.factor*super().cost()
s=MyStock('GOOG',100,490.10,1.25)
print(s.cost())

# isinstance
class Shape:
    pass
class Circle(Shape):
    pass
c = Circle()
print(isinstance(c, Circle))   # True
print(isinstance(c, Shape))    # True
print(isinstance(c, object))   # True

print(type(c) is Circle)
print(type(c) is Shape)
print(type(c) is object)

print(Circle.__mro__)