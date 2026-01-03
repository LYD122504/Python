a=[1,2,3,4]
b=(2*x for x in a)
print(a)
print(b)
for i in b:
    print(i,end=' ')
print()
print(sum(x*x for x in a))
a=[1,2,3,4]
b=(x*x for x in a)
c=(-x for x in b)
for i in c:
    print(i,end=' ')