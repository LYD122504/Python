# Exercise 7.1 A simple example of variable arguments
def avg(x,*more):
    return float(x+sum(more))/(1+len(more))
print(avg(10,11))
print(avg(3,4,5))
print(avg(1,2,3,4,5,6))
# Exercise 7.2 Passing tuple and dicts as arguments
from stock import stock
data=('GOOG',100,490.91)
s=stock(*data)
data={'name':'GOOG','shares':100,'price':490.91}
s=stock(**data)