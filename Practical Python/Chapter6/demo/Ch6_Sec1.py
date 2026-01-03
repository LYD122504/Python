a='hello'
for c in a:
    print(c)# Loop over characters in a
b={'name':'Dave','password':'foo'}
for k in b:# Loop over keys in dictionary
    print(k)
c=[1,2,3,4]
for i in c:# Loop over items in a list/tuple
    print(i)

'''
f=open('foo.txt')
for x in f:
print(x)
'''
# 迭代底层行为
_iter=a.__iter__()# Get iterator object
while True:
    try:
        x=_iter.__next__()#Get next item
        print(x)
    except StopIteration: #No more items
        break

x=[1,2,3]
it=x.__iter__()
print(type(it))
print(it)
for i in range(len(x)):
    print(it.__next__())
it=a.__iter__()
print(list(it))
print(list(it))

class Count:
    def __init__(self,n):
        self.n=n
        self.i=0
    def __iter__(self):
        return self
    def __next__(self):
        if self.i>=self.n:
            raise StopIteration
        val=self.i
        self.i+=1
        return val
    
for x in Count(3):
    print(x)