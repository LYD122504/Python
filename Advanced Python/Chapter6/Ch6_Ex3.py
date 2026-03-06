def func(a, b):
    'This function does something.'
    pass
print(func.__doc__)
help(func)
def foo(a:int,b:str)->str:
    pass
print(foo.__annotations__)
func.threadsafe = False
func.blah = 42
print(func.__dict__)
def foo(arg1, arg2, arg3, *args, kwarg1="FOO", kwarg2="BAR", kwarg3="BAZ"):
    pass
print(foo.__kwdefaults__)

def func(a, b,*, c=42):
    'This function does something.'
    pass
print(func.__name__)
print(func.__defaults__)
print(func.__kwdefaults__)
print(func.__code__)
print(func.__code__.co_argcount)
print(func.__code__.co_varnames)
print(dir(func))

import inspect
def func(a,b=10,*args,**kwargs):
    pass
# 获取函数签名
sig=inspect.signature(func)
print(sig)
# 获取参数信息
for name,param in sig.parameters.items():
    print(f"{name}: {param.default}")
import inspect
import sys
# 定义测试对象
def my_function(x, y):
    return x + y
class MyClass:
    def instance_method(self):
        pass
    @classmethod
    def class_method(cls):
        pass
    @staticmethod
    def static_method():
        pass
my_instance = MyClass()
# 内置模块和函数
import math
# 执行类型检查
print("=" * 50)
print("inspect 类型检查函数验证")
print("=" * 50)
print(f"\n1. inspect.isfunction(my_function):")
print(f"   结果: {inspect.isfunction(my_function)}")
print(f"   说明: my_function 是普通函数 ✓")
print(f"\n2. inspect.isclass(MyClass):")
print(f"   结果: {inspect.isclass(MyClass)}")
print(f"   说明: MyClass 是类 ✓")

print(f"\n3. inspect.ismodule(sys):")
print(f"   结果: {inspect.ismodule(sys)}")
print(f"   说明: sys 是模块 ✓")

print(f"\n4. inspect.ismethod(my_instance.instance_method):")
print(f"   结果: {inspect.ismethod(my_instance.instance_method)}")
print(f"   说明: 绑定到实例的方法是方法 ✓")

print(f"\n5. inspect.isbuiltin(len):")
print(f"   结果: {inspect.isbuiltin(len)}")
print(f"   说明: len 是内置函数 ✓")

# 补充对比测试
print("\n" + "=" * 50)
print("补充对比测试")
print("=" * 50)
print(f"\ninspect.isfunction(MyClass.instance_method):")
print(f"   结果: {inspect.isfunction(MyClass.instance_method)}")
print(f"   说明: 未绑定的类方法是函数")
print(f"\ninspect.isfunction(my_instance.static_method):")
print(f"   结果: {inspect.isfunction(my_instance.static_method)}")
print(f"   说明: 静态方法被视为函数")
print(f"\ninspect.ismethod(MyClass.class_method):")
print(f"   结果: {inspect.ismethod(MyClass.class_method)}")
print(f"   说明: 类方法也是方法")
print(f"\ninspect.isbuiltin(math.sqrt):")
print(f"   结果: {inspect.isbuiltin(math.sqrt)}")
print(f"   说明: math.sqrt 是内置函数")
# 批量检查示例
print("\n" + "=" * 50)
print("批量类型检查示例")
print("=" * 50)
objects = {
    '普通函数': my_function,
    '类': MyClass,
    '实例方法': my_instance.instance_method,
    '类方法': MyClass.class_method,
    '静态方法': my_instance.static_method,
    '内置函数': len,
    '模块': sys,
    '字符串': "hello",
    '整数': 42,
}
for name, obj in objects.items():
    checks = {
        'isfunction': inspect.isfunction(obj),
        'ismethod': inspect.ismethod(obj),
        'isclass': inspect.isclass(obj),
        'ismodule': inspect.ismodule(obj),
        'isbuiltin': inspect.isbuiltin(obj),
    }
    result = ', '.join([k for k, v in checks.items() if v])
    print(f"{name:10s}: {result if result else '无匹配类型'}")
# 获取源代码（字符串）
source = inspect.getsource(func)
# 获取源文件路径
file_path = inspect.getfile(func)
# 获取代码行号
line_no = inspect.getsourcelines(func)[1]
print(source)
print(file_path)
print(line_no)
sig = inspect.signature(func)
args = (1, 2)
kwargs = {'c': 10}
bound = sig.bind(*args, **kwargs)
for name, val in bound.arguments.items():
    print(name, '=', val)

# Inspecting functions
def add(x,y):
    'Adds two things'
    return x+y
print(dir(add))
print(add.__name__)
print(add.__module__)
print(add.__doc__)
print(add.__code__)
print(add.__code__.co_argcount)
print(add.__code__.co_varnames)
# Using the inspect module
import inspect
sig=inspect.signature(add)
print(sig)
print(sig.parameters)
print(tuple(sig.parameters))
# Putting it Together
import inspect
import stock
sig=inspect.signature(stock.Stock)
print(tuple(sig.parameters))
s = stock.Stock(name='GOOG', shares=100, price=490.1)
print(s)
print(s.shares)
s.shares=100
