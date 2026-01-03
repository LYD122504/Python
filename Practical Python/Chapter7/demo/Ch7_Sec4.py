def add(x,y):
    return x+y
print(add(2,3))
def add(x,y):
    print("Calling add function")
    return x+y
print(add(5,7))
def sub(x,y):
    print("Calling sub function")
    return x-y
print(sub(10,4))
def logged(func):
    def wrapper(*args, **kwargs):
        print('Calling',func.__name__,'functions')
        return func(*args, **kwargs)
    return wrapper
def add(x,y):
    return x+y
add=logged(add)
print(add(3,4))
@logged
def sub(x,y):
    return x-y
print(sub(9,2))