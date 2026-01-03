import Mro
class LogginMixin:
    def log(self,msg):
        print(f"[LOG]:{msg}")

class AuthMixin:
    def authenticate(self,user):
        print(f"Authenticating {user}")

class User(LogginMixin,AuthMixin):
    def __init__(self,name):
        self.name=name

u=User('Alice')
u.log("User created")
u.authenticate("Alice")

# 旧式MRO算法 DFS算法
class A:
    def foo(self):
        print("Here is a A")

class B(A):
    def foo(self):
        print("Here is a B")
        A.foo(self)
    
class C(A):
    def foo(self):
        print("Here is a C")
        A.foo(self)

class D(B,C):
    def foo(self):
        print("Here is a D")
        B.foo(self)
        C.foo(self)

d=D()
d.foo()
print(D.__mro__)
# 旧式MRO算法
OldMro=Mro.old_mro(D,[])
print(OldMro)
# 旧式MRO加上去重
ImOldMro=Mro.improve_mro(D,[])
print(ImOldMro)
# C3 算法
C3Mro=Mro.C3Mro(D)
print(C3Mro)
# 复杂的多继承
class D: pass
class E: pass
class F: pass
class B(D,E):pass
class C(D,F):pass
class A(B,C):pass

print(Mro.C3Mro(A))