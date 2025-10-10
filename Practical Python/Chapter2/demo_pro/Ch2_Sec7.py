# assignment
a=[1,2,3]
b=a
c=[a,b]
print(b)
print(c)
b.append(10)
print(a)
print(b)
print(c)
a=[2,3,4]
print(a)
print(b)
print(c)

# Identity and references
a=[1,2,3]
b=a
print(a is b)
print(id(a),id(b))
c=[1,2,3]
print(a is c)
print(a==c)
print(id(a),id(c))
a.append(10)
print(a)
print(b)
print(c)

# List and Dict
a=[1,2,[1,[2],3],3]
#b=a
#print(a is b)
#print(id(a),id(b))
b=list(a)
print(a is b)
print(id(a),id(b))
a[1]=10
print(a[1] is b[1])
print(b)
import copy
b=copy.deepcopy(a)
print(a is b)
print(a[2] is b[2])

if isinstance(a, list):
    print('a is a list')
if isinstance(a, (list,tuple)):
    print('a is a list or tuple')

import math
items=[abs,math,ValueError]
print(items)
print(items[0](-10))
print(items[1].sqrt(16))
try:
    x=int('not a number')
except items[2]:
    print('Not a number')
