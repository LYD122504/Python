x=1
def func():
    test=1
    print(globals())
    print(locals())
print(globals())
print(locals())
func()
import stock
s = stock.Stock('GOOG', 100, 490.1)
print(s)
help(stock.Stock)