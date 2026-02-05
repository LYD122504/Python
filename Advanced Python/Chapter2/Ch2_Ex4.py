#string adapt
import sys
a = 'n'
b = 'ñ'
print(sys.getsizeof(a))
print(sys.getsizeof(b))
#memory overhead
a = 2
print(sys.getsizeof(a))
b = 2.5
print(sys.getsizeof(b))
c = '2.5'
print(sys.getsizeof(c))
#operations
a=2
b=3
print(a+b)
print(a.__add__(b))
c='Hello '
print(len(c))
print(c.__len__())
# object protocols
def foo(x):
    print('Foo:', x)
def bar(x,y):
    return x+y
import dis
print(dis.dis(foo))
print(dis.dis(bar))
# make new built
from fractions import Fraction
a=Fraction(1,3)
b=Fraction(2,5)
print(a+b)
print(a>0.5)
from functools import total_ordering

@total_ordering
class MutInt:
    __slots__=['value']
    # Mutable Integers
    def __init__(self,value=0):
        self.value=value
    # Fixing output
    def __str__(self):
        return str(self.value)
    # !r的作用是在f-string中调用repr()
    # !s的作用是在f-string中调用str()
    # !a的作用是在f-string中调用ascii()
    def __repr__(self):
        return f'MutInt({self.value!r})'
    # 用于f-string,string.format()做格式化自动调用
    def __format__(self,fmt):
        return format(self.value,fmt)
    # Math Operator
    def __add__(self,other):
        if isinstance(other,MutInt):
            return MutInt(self.value+other.value)
        if isinstance(other,int):
            return MutInt(self.value+other)
        else:
            raise NotImplemented
        
    __radd__=__add__# Reversed operands

    def __iadd__(self,other):
        if isinstance(other,int):
            self.value+=other
            return self
        if isinstance(other,MutInt):
            self.value+=other.value
            return self
        else:
            raise NotImplemented
    # Comparisons
    def __eq__(self,other):
        if isinstance(other,int):
            return self.value==other
        if isinstance(other,MutInt):
            return self.value==other.value
        else:
            raise NotImplemented
    def __lt__(self,other):
        if isinstance(other,int):
            return self.value<other
        if isinstance(other,MutInt):
            return self.value<other.value
        else:
            raise NotImplemented
    # Coversions
    def __int__(self):
        return self.value
    def __float__(self):
        return float(self.value)
    __index__=__int__
            
a=MutInt(5)
print(a)
print(repr(a))
print(a.value)
a.value=10
print(a.value)
print(f'The value is {a:*^10d}')
print(1+a)
b=MutInt(2)
print(a+b)
a=MutInt(3)
b=a
a+=10
print(a)
print(b)
a=[1,2,3]
b=a
a+=[4,5]
print(a)
print(b)
a=(1,2,3)
b=a
a+=(4,5)
print(a,b)
a=MutInt(3)
b=MutInt(3)
print(a==b)
print(a==3)
print(a>2)
print(int(a))
print(float(b))
name=['Dave','Guido','Paula','Thomas','Lewis']
a=MutInt(1)
print(name[a])
# 内存开销
a=12.33
import sys
print(sys.getsizeof(a))
print(sys.getsizeof(0))
print(sys.getsizeof(2**90-1))