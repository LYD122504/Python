class A:
    pass
class B:
    pass
class C(A):
    pass
class D(B,C):
    pass
print(D.__base__)
# MRO
class A(object): pass
class B(A): pass
class C(A): pass
class D(B): pass
class E(D): pass
print(E.__mro__)
class A(object): pass
class B(object): pass
class C(A,B): pass
class D(B): pass
class E(C,D): pass
print(E.__mro__)

# Rule1:兼容的方法参数
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

# 测试
try:
    c = C()
    c.spam(1, 2)
except TypeError as e:
    print(f"错误: {e}\n")

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
# The directions of inheritance
class A:
    def spam(self):
        print('A.spam')
class B(A):
    def spam(self):
        print('B.spam')
        super().spam()
class C(B):
    def spam(self):
        print('C.spam')
        super().spam()
print(C.__mro__)
c=C()
c.spam()
class Base:
        def spam(self):
            print('Base.spam')

class X(Base):
    def spam(self):
        print('X.spam')
        super().spam()
class Y(Base):
    def spam(self):
        print('Y.spam')
        super().spam()
class Z(Base):
    def spam(self):
        print('Z.spam')
        super().spam()
class M(X,Y,Z):
    pass
print(M.__mro__)
m=M()
m.spam()
class N(Z,Y,X):
    pass
print(N.__mro__)
n=N()
n.spam()
import validate
print(validate.Integer.check(10))
print(validate.String.check('10'))
def add(x,y):
    validate.Integer.check(x)
    validate.Integer.check(y)
    return x+y
print(add(2,2))
print(validate.PositiveInteger.check(20))
print(validate.NonEmptyString.check('hello'))