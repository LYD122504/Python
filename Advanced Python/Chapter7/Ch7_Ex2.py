def add(x, y):
    'Adds x and y'
    return x + y
print(add.__name__)
print(add.__doc__)
# help(add)
def logged(func):
    def wrapper(*args,**kwargs):
        print('Calling',func.__name__)
        return func(*args,**kwargs)
    return wrapper
@logged
def add(x, y):
    'Adds x and y'
    return x + y
print(add.__name__)
print(add.__doc__)
def logged(func):
    def wrapper(*args,**kwargs):
        print('Calling',func.__name__)
        return func(*args,**kwargs)
    wrapper.__name__=func.__name__
    wrapper.__doc__=func.__doc__
    return wrapper
@logged
def add(x, y):
    'Adds x and y'
    return x + y
print(add.__name__)
print(add.__doc__)
from functools import wraps
def logged(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        print('Calling',func.__name__)
        return func(*args,**kwargs)
    return wrapper
@logged
def add(x, y):
    'Adds x and y'
    return x + y
print(add.__name__)
print(add.__doc__)
def logmsg(message):
    def logged(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            print(message.format(name=func.__name__))
            return func(*args,**kwargs)
        return wrapper
    return logged
@logmsg('You called {name}')
def add(x,y):
    return x+y
print(add(3,4))
logged=logmsg('You called {name}')
@logged
def add(x,y):
    return x+y
print(add(3,4))
# Copying Metadata
@logged
def add(x,y):
    'Adds two things'
    return x+y
print(add)
# help(add)
print(add.__doc__)
# Your first decorator with arguments
import sample
print(sample.add(2,3))
print(sample.mul(2,3))
# Multiple decorators and methods
from logcall import logged
from functools import wraps
class Spam:
    @logged
    def instance_method(self):
        pass
    
    @classmethod
    @logged
    def class_method(cls):
        pass

    @staticmethod
    @logged
    def static_method():
        pass

    @property
    @logged
    def property_method(self):
        pass
s=Spam()
s.instance_method()
Spam.class_method()
Spam.static_method()
s.property_method
# Validation (Redux)
import validate
@validate.validated
def add(x: validate.Integer, y:validate.Integer) -> validate.Integer:
    return x + y
add(2,3)
@validate.enforce(x=validate.Integer,y=validate.Integer,return_c=validate.Integer)
def add(x, y):
    return x + y
add(2,3)