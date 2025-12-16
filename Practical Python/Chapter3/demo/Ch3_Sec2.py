def square(x):
    x=x+1
    return x*x
x=2
a=square(x)
print(a,x)

def divide(a,b):
    q=a//b
    r=a%b
    return q,r
x,y=divide(37,5)
print('x=',x,'y=',y)
x=divide(43,3)
print(x)

name = 'Dave'

def spam():
    name = 'Guido'

spam()
print(name) # prints 'Dave'

def foo(items):
    items.append(42)
def bar(items):
    items=[1,2,3]
    
a=[1,2,3]
foo(a)
print(a)
bar(a)
print(a)
