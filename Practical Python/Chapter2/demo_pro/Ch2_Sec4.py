a='Hello' # String
b=[1,4,5] # List
c=('GOOG',100,490.1)

# Indexed order
print(a[0])
print(b[-1])
print(c[1])

# Length of sequence
print(len(a))
print(len(b))
print(len(c))

print(a*3)
print(b*2)
print(c*2)

a=(1,2,3)
b=(2,3,4)
print(a+b)
#c=[2,3,4]
#print(a+c)

a=list(range(9))
print(a)

print(a[2:5])
print(a[-5:])
print(a[:3])

a=(0,1,2,3,4,5,6,7,8,9)
print(a[2:5])

b=list(a)
b[2:5]=[10,11,12,13,14]
print(b)
del b[2:5]
print(b)

#s='Hello'
#print(sum(s))
#print(min(s))
#print(max(s))

t = ['Hello', 'World']
print(max(t))
print(max(max(t)))

s=[1,4,9,16]
for i in s:
    print(i)
print(i)

for i in range(10):
    print(i*i)
for j in range(10,20):
    print(j)
for k in range(10,51,2):
    print(k)

names=['Elwood','Jake','Curtis']
for i,name in enumerate(names):
    print('i=',i,'name=',name)
for i,name in enumerate(names,start=1):
    print('i=',i,'name=',name)

t=((1,2),2,3,4,5,6,'a')
for i in t:
    print(i)

points = [
  (1, 4),(10, 40),(23, 14),(5, 6),(7, 8)
]
for x in points:
    print(x)

for x, y in points:
    print(x,y)

columns = ['name', 'shares', 'price']
values = ['GOOG', 100, 490.1 ]
pairs = zip(columns, values)
