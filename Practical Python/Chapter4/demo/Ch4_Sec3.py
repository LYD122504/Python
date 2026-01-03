class A:
    pass

a = A()
print(repr(a))

x=10
print(eval("x+1"))

print(eval("x+1",{"x":10}))
print(eval("a + b", {"b": 2}, {"a": 1}))   #li 3