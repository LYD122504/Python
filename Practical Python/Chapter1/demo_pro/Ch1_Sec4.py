# 1.3 String

# Single quote
a='Yeah but no but yeah but...'
print(a)

# Double quote
b="Computer says no"
print(b)

#Triple quotes
c = '''
Look into my eyes, look into my eyes, the eyes, the eyes, the eyes,
not around the eyes,
don't look around the eyes,
look into my eyes, you're under.
'''
print(c)

def add(a, b):
    """
    这个函数用于计算两个数的和
    参数:
        a: 第一个数字
        b: 第二个数字
    返回:
        两个数字的和
    """
    return a + b

help(add)  # 查看函数的文档字符串
print(add.__doc__)

a='\xf1'
print(a)

b='\u2200'
print(b)

c='\U0001D122'
print(c)

d = '\N{FOR ALL}'   # d = '∀'
print(d)

a='Hello world'
print(a[0])
print(a[3])
print(a[-1])

d = a[:5]     # 'Hello'
e = a[6:]     # 'world'
f = a[3:8]    # 'lo wo'
g = a[-5:]    # 'world'
print(d,e,f,g)

# Concatenation
a='Hello'+'World'
print(a) 
b='Say'+a
print(a,b)

#Length
print(len(a))

#Membership test (in/not in)
t='e' in a
f='x' in a
g='hi' not in a
print(t,f,g)
print(type(t))

#Replication(s*n)
rep=a*2
print(rep)

a='   Hello   '
print(a)
print(a.strip())
print(a)

s = 'Hello world'
t = s.replace('Hello' , 'Hallo')   # 'Hallo world'
print(t)

b = b"hello"

print(b[0])          # 104，ASCII 'h'
print(b[:2])         # b'he'
print(len(b))        # 5

# 字符串编码为 bytes
s = "你好"
b_utf8 = s.encode("utf-8")
print(b_utf8)        # b'\xe4\xbd\xa0\xe5\xa5\xbd'

# bytes 解码为字符串
s2 = b_utf8.decode("utf-8")
print(s2)            # 你好


a="He said, 'Hello!'"
print(a)
b='She replied, "Hi!"'
print(b)

b = b"ABC"
print(b[1])         # b'ABC'
print(type(b))   # <class 'bytes'>

s='Hello'
bstr=s.encode('utf-8') # 普通字符串转换为字节字符串
print(bstr) # b'Hello'
s2=bstr.decode('utf-8') # 字节字符串转换为普通字符串
print(s2) # 'Hello'

a=r"abc\\\\"   # 语法错误
print(a)
b=r"abc\\"  # 可以，表示 abc\

value = 1234.56789
print(f"{value:.2f}")   # 保留两位小数 → 1234.57
print(f"{value:10.2f}") # 宽度10，右对齐 → "   1234.57"
print(f"{value:<10.2f}")# 宽度10，左对齐 → "1234.57   "
ratio=0.456
print(f"{ratio:.1%}")# 百分比格式 → 45.6%
num=42
print(f"{num:05d}") # 十六进制格式 → 00042

person = {"name": "Bob", "age": 30}
print(f"{person['name']} is {person['age']} years old.")  # Bob is 30 years old


print(f"{'Hello\n'}") # 也可以，但没必要