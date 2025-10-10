# 1.2 Numbers
a=True
b=False
print(type(a))
print(type(b))

c=4.0*False
d=False
print(c)
print(type(c))
print(type(d))
if d==0:
    print("d is False")

a=2.1+4.2
print(a==6.3)
print(a)

a=1
b=2
c=3
if(b>=a and b<=c):
    print("b is between a and c")
if not(b<a or b>c):
    print("b is still between a and c")