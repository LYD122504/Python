def add(x,y):
    def do_add():
        print(f'{x}+{y}->{x+y}')
    return do_add
a=add(3,4)
print(a)
print(a.__closure__)
print(a.__closure__[0].cell_contents)
print(a.__closure__[1].cell_contents)
a()
def new_add(x,y):
    result=x+y
    def get_result():
        return result
    return get_result
b=new_add(3,4)
print(b.__closure__)
print(type(b.__closure__))
print(b.__closure__[0].cell_contents)
def counter(n):
    def incr():
        nonlocal n
        n+=1
        return n
    return incr
c=counter(10)
print(c())
print(c())
# 延迟求值:延迟计算直到真正需要时候才执行
def delayed_computation(x,y):
    print('Prepared Done')
    def compute():
        print("Performing computation")
        return x+y
    return compute
result_func=delayed_computation(10,20)
print(result_func())
# 回调函数:闭包携带上下文信息,适合用作回调
def make_callback(name,value):
    def callback():
        print(f'Callback {name}: value = {value}')
    return callback
cb1=make_callback('handler1',100)
cb2=make_callback('handler2',200)
cb1()
cb2()
def create_event_handler(event_name,handler_data):
    def handler(event):
        print(f"Event '{event_name}' triggered")
        print(f"Data: {handler_data}")
        print(f"Event details: {event}")
    return handler
click_handler=create_event_handler("click",{'count':0})
click_handler({'x':100,'y':200})

def make_multiplier(factor):
    def multiplier(x):
        return x*factor
    return multiplier
double=make_multiplier(2)
triple=make_multiplier(3)
percent=make_multiplier(0.01)
print(double(10))
print(triple(10))
print(percent(10))
def make_formatter(prefix, suffix):
    """生成一个带前缀和后缀的格式化函数"""
    def formatter(text):
        return f"{prefix}{text}{suffix}"
    return formatter

# 生成不同的格式化器
bold = make_formatter("**", "**")
italic = make_formatter("*", "*")
quote = make_formatter("> ", "")

print(bold("Hello"))    # **Hello**
print(italic("World"))  # *World*
print(quote("Note"))    # > Note

def counter(start=0):
    """创建一个计数器闭包"""
    count = start
    def increment(step=1):
        nonlocal count
        count += step
        return count
    return increment

c = counter(10)
print(c())  # 11
print(c())  # 12
print(c(5)) # 17
# Closures as a data structure
def counter(value):
    def incr():
        nonlocal value
        value+=1
        return value
    def decr():
        nonlocal value
        value-=1
        return value
    return incr,decr
up,down=counter(0)
print(up())
print(up())
print(up())
print(down())
print(down())

# Closures as a code generator

import stock
ds=stock.DeStock('AA',100,490.1)
