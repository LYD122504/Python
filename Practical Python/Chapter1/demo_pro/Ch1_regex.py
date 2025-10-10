import re
# re模块的基本函数

# re.match函数指从字符串的开头开始匹配,如果开头不符合,那么就直接返回None
print(re.match(r"\d+","abc456"))
print(re.match(r"\d+","123abc456"))

# re.search函数指扫描整个字符串,找到第一个匹配的位置;不要求一定要在字符串开头.
print(re.search(r"\d+","abc123def456"))

# re.findall函数扫描整个字符串,并返回所有匹配的字符串列表
print(re.findall(r"\d+","abc123def456"))

# re.finditer返回的是一个迭代器,每个元素是Match对象
for m in re.finditer(r"\d+","abc123def456"):
    print(f"匹配到的子字符串:{m.group()};位置:{m.span()}")

# re.fullmatch函数要求整个字符串必须完全匹配
print(re.fullmatch(r"\d+","123"))
print(re.fullmatch(r"\d+","123a"))

# re.split函数按照模式分割字符串
print(re.split(r"\s+","abc def ghi"))

# re.sub函数替换匹配的部分
print(re.sub(r"\d+","#","a12b34"))

# re.subn函数返回(替换后字符串,替换次数)
print(re.subn(r"\d+","#","a12b34"))

# Match 对象常用属性
m=re.search(r"\d+","abc123def456")
print(m.group())
print(m.start())
print(m.end())
print(m.span())

pattern=re.compile(r"\d+")
text="Order123, Item456, Code789"
print(pattern.findall(text))
for m in pattern.finditer(text):
    print(m.group(),m.span())

# 忽略大小写匹配
print(re.fullmatch("abc","ABC",re.I))

# 多行模式
text='''First line
Second line
Third line'''
print(re.findall(r"^Second",text))
print(re.findall(r"^Second",text,re.M))

# 点号匹配换行符
text="Line1\nLine2\nLine3"
print(re.findall(r"Line.*",text))
print(re.findall(r"Line.*",text,re.S))

pattern = re.compile(r"""
    \d+     # 匹配一个或多个数字
    \s*     # 允许有空格
    [a-zA-Z]+  # 再跟着字母
""", re.X)

print(pattern.findall("123abc  456  def"))
# ['123abc', '456def']
