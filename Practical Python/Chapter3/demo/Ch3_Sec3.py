def add(x,y):
    return x+y

print(add(3,4))
print(add('Hello',' World'))
print(add('3','4'))

def foo():
    raise RuntimeError('Invalid user name')

def bar():
    try:
        foo()
    except RuntimeError as e:
        print('Failed : Reason',e)

bar()

name='David'
def fun():
    name='Guide'
    return name
test=fun()
print(name)