import logcall
@logcall.logged
def add(x,y):
    return x+y
@logcall.logged
def sub(x,y):
    return x-y
@logcall.logformat('{func.__code__.co_filename}:{func.__name__}')
def mul(x,y):
    return x*y