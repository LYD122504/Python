import math
import urllib.request

def sumcount(n):
    '''
    Return the sum of the first n integers
    '''
    total=0
    while n>0:
        total+=n
        n-=1
    return total
a=sumcount(100)
print(a)

x=math.sqrt(5)
print(x)

u = urllib.request.urlopen('http://www.python.org/')
data = u.read()
print(data[:50])

try:
	raise RuntimeError('What a kerfuffle')
except RuntimeError:
	print("异常处理完成")