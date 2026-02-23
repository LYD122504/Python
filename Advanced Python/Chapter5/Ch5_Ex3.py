def sum_squares(nums):
    total=0
    for n in nums:
        total+=n*n
    return total
def sum_cubes(nums):
    total=0
    for n in nums:
        total+=n**3
    return total

def sum_map(func,nums):
    total=0
    for n in nums:
        total+=func(n)
    return total
def square(x):
    return x*x
nums=[1,2,3,4]
r=sum_map(square,nums)
print(r)
cube=sum_map(lambda x:x**3,nums)
print(cube)
def distance(x,y):
    return abs(x-y)
print(distance(10,20))
distance_from10=lambda y:distance(10,y)
print(distance_from10(3))
print(distance_from10(14))
from functools import partial
distance10=partial(distance,10)
print(distance10(2))
from functools import partial
def power(base, exponent):
    return base ** exponent
square = partial(power, exponent=2)
cube   = partial(power, exponent=3)
print(list(map(square, [1, 2, 3])))  # [1, 4, 9]
print(list(map(cube,   [1, 2, 3])))  # [1, 8, 27]

def map(func, values):
    return [func(x) for x in values]

def reduce(func, values, initial=0):
    result = initial
    for n in values:
        result = func(n, result)
    return result

nums = [1, 2, 3, 4]
result = reduce(lambda x, y: x + y, map(lambda x: x * x, nums))  # 30
print(result)

import reader
from stock import Stock
def make_dict(row,headers):
    return dict(zip(headers,row))
with open('../Data/portfolio.csv') as lines:
    #Dictresult=reader.convert_csv(lines,make_dict)
    Stockresult=reader.convert_csv(lines,Stock.from_row)
#print(Dictresult)
print(Stockresult)
# Mapping
nums=[1,2,3,4]
squares=map(lambda x:x*x,nums)
for n in squares:
    print(n)