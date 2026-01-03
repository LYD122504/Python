import time
def timethis(func):
    def wrapper(*argc,**kwargs):
        start=time.time()
        r=func(*argc,**kwargs)
        end=time.time()
        print('%s.%s: %f' % (func.__module__, func.__name__, end-start))
        return r
    return wrapper