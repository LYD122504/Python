---
title: Pratical Python-Strings
date: 2025-09-03 21:42:15
tags:
    - Computer Science
    - Python
categories: Python
mathjax: true
---

本笔记完全基于David Beazley的Python教程-[Practical Python](https://dabeaz-course.github.io/practical-python/Notes/Contents.html).

## Strings

Python与C/C++不同在于他并没有char类型,因此对于Python的字符串而言,他可以用单引号或者双引号来引导字符串.Python的字符串通常只能传入单行,遇到换行符会报错;但可以通过三引号来表示多行字符串,例如:

<!--more-->

```python
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
```

但我们前面提到的多行注释也可以用三引号表示,这是因为Python其实并没有多行注释的专用符号,我们通过三引号引导的多行字符串对程序进行解释,但不做赋值操作,程序会阅读后并不保存相关数据,也就认为其可用于注释.其次我们用三引号引导的字符串做注释的时候,如果其出现在函数,模块或者类的开头,那么其会被认作是该代码的文本字符串,我们可以通过.\_\_doc\_\_属性或者help函数来查看:

```python
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
```

正是因为Python的字符串可以用单引号或双引号引导,因此我们可以不借助转义符来表示字符串中包含引号的情况,例如:

```python
a="He said, 'Hello!'"
b='She replied, "Hi!"'
```

但是如果字符串中既包含单引号又包含双引号,那么我们还是需要用转义符\\来表示.

在C/C++中,字符串的每个字符在计算机内部都是以ASCII编码的形式存储的,当然更为现代的版本也是支持了UTF8编码.同样Python的字符串也是以Unicode编码形式存储的,或者说我们可以给程序一个字符的unicode编码,程序会将其转换为对应字符后存储.

```python
a='\xf1' # \x表示后面跟的是一个十六进制的数字,其后f1表示两个字节
b='\u2200' # \u表示是unicode编码,其后接的2200是四个十六进制数字,表示其码点为8704
c='\U0001D122' # \u和\U都表示unicode编码,但是\U后面需要接8个十六进制数字,不足8位需要在前面补0,其码点为119074
d='\N{FOR ALL}' # \N{}是通过字符名称来表示字符,其字符名称必须是Unicode标准中定义的名称
```

对于字符串索引,同样字符串也是从0开始索引,但与C/C++不同的是,Python支持负数索引,负数索引表示从字符串的末尾开始向前索引.例如,-1表示字符串的最后一个字符,-2表示导数第二个字符,以此类推:

```python
s='Hello world'
print(s[0]) # H
print(s[-1]) # d
print(s[-5]) # w
```

Python也支持利用:指定字符串检索范围来作切片操作或者提取子字符串,若存在缺省指标,则默认为字符串的开头或者结尾,这里值得注意的是s[start:end]会包含start的索引,但不包含end:

```python
d = s[:5]     # 'Hello'
e = s[6:]     # 'world'
f = s[3:8]    # 'lo wo'
g = s[-5:]    # 'world'
```

Python的字符串操作有+(链接两个字符串),len(求字符串长度),in/not in(检查子字符串是否在字符串中出现过)和\*(重复字符串):

```python
# Concatenation
a='Hello'+'World' # 'HelloWorld'
b='Say'+a # 'SayHelloWorld'
# Length
print(len(a)) # 10
# Membership test(in/not in)
t='e' in a # True,bool类型
f='x' in a # False,bool类型
g='hi' not in a # True,bool类型
# Replication(s*n)
rep=a*2 # 'HelloWorldHelloWorld',他主要是同一个字符串的重复,类似于a+a+...+a(n个a相加)
```

Python的字符串还有很多内置的方法,可以通过.来调用,例如:

```python
s.endswith(suffix)     # 检查字符串后缀是否为suffix,如果有则返回True,否则返回False
s.find(t)              # 在字符串s中查找字符串t第一次出现的位置,如果找不到返回-1
s.index(t)             # 在字符串s中查找字符串t第一次出现的位置,如果找不到返回异常ValueError
s.join(slist)          # 以字符串s作为分隔符,将字符列表的所有元素连接成一个新的字符串
s.replace(old,new)     # 替换字符串s中所有old子字符串为new子字符串,返回一个新的字符串
s.rfind(t)             # 从字符串s的末尾开始查找字符串t最后一次出现的位置,如果找不到返回-1
s.rindex(t)            # 从字符串s的末尾开始查找字符串t最后一次出现的位置,如果找不到返回异常ValueError
s.split([delim])       # 以delim为分隔符切片s,如果不指定delim,则以空白字符(空格,换行,制表符等)为分隔符
s.startswith(prefix)   # 检查字符串前缀是否为prefix,如果有则返回True,否则返回False
s.strip()              # 删除字符串s两端的空白字符(空格,换行,制表符等),返回一个新的字符串
```

值得注意的是,Python的字符串是不可改变的,也就是我们不能通过索引赋值和方法来修改已有的字符串,只能通过对整体的重新赋值来改变字符串的值,如:

```python
s='  Hello   '
print(s.strip()) # 'Hello'
print(s) # '  Hello   ',原字符串并没有改变
```

对于上面罗列的方法,我们需要指出以下几点:

1.  join方法中传入的slist一定要是一个字符串列表,否则会报错.
2.  find和index方法的作用其实一样,但是唯一的不同在于find返回的是-1,而index会报出异常.因此在不确定子字符串是否存在的情况下,建议使用index方法.
3.  在replace方法中,如果old子字符串在s中不存在,他并不会报错,返回的值仍然是原字符串s.

Python在普通的字符串之外还提供几类特殊的字符串,如字节字符串,原始字符串和格式化字符串.

字节字符串(byte string)是以b或者B开头的字符串,其是以字节为单位进行存储的,每个元素默认是0-255之间的整数,适合处理二进制数据,网络传输或者文件I/O等操作.他和普通字符串最大的区别在于,在Python3中,普通字符串依靠Unicode编码,每个字符可以是汉字,英文或者特殊符号等;而字节字符串并不依赖编码规则,而是直接存储字节,因为计算机中存储的最小单元就是字节,所以字节字符串可以存储更多类型的内容,如视频,音频等等.

```python
bstr=b'Hello' # 字节字符串
print(bstr) # b'Hello'
print(bstr[0]) # 72,字节字符串的每个元素是0-255之间的整数
print(bstr[1:4]) # b'ell',字节字符串的切片操作返回的仍然是字节字符串
```

字节字符串并不能与普通字符串进行链接,否则会报类型错误;可以用索引访问每个字节,但是如果访问的是一个元素,返回的是字节对应的整数值,如果访问的是一个切片,返回的则是字节字符串.字节字符串和普通字符串之间可以通过encode和decode方法进行转换,如:

```python
s='Hello'
bstr=s.encode('utf-8') # 普通字符串转换为字节字符串
print(bstr) # b'Hello'
s2=bstr.decode('utf-8') # 字节字符串转换为普通字符串
print(s2) # 'Hello'
```

这里的utf-8表示编码格式,当然也可以使用其他编码格式,如ascii,latin1等.

原始字符串(raw string)是以r或者R开头的字符串,其最大的特点在于字符串中的转义字符并不会被处理,换言之,他不会处理字符串中出现的\\和其后面的字符,而是将其作为普通字符进行存储.如:

```python
rs=r'C:\newfolder\test.txt' # 原始字符串
print(rs) # C:\newfolder\test.txt
```

字符串是括号内包围的原始文本,与输入完全一致.这在反斜杠具有特殊意义的情况下很有用.例如:文件名,正则表达式等.原始字符串有如下的特点需要注意:

1.  原始字符串不能以奇数个反斜杠结尾,因为这样最后一个反斜杠就不会有任何字符与之配对,会自动匹配引号,从而导致字符串没有结束符而报错.

2.  字符串前的r/R只影响转义,不会影响字符串内容的其他特性.

    ```python
    r'C:\path\to\file\\' # 正确,以偶数个反斜杠结尾
    r'C:\path\to\file\' # 错误,以奇数个反斜杠结尾,会报错
    len(r'Hello\nWorld') # 12,原始字符串中的\n不会被处理为换行符
    len('Hello\nWorld') # 11,普通字符串中的\n被处理为换行符 
    ```
    
    

格式化字符串(f-string)是以f或者F开头的字符串,其允许在字符串中嵌入表达式,这些表达式会在运行时被计算并替换为其结果.

```python
name='Alce'
age=25
print(f"My name is {name}, I am {age} years old.") # My name is Alce, I am 25 years old.
```

其基本的用法如下:

```python
# 表达式
a, b = 5, 10
print(f"{a}+{b}={a+b}") # 5+10=15
# 函数调用
import math
print(f"pi={math.pi:.2f}") # pi=3.14,保留两位小数
# 格式化
value = 1234.56789
print(f"{value:.2f}")   # 保留两位小数 → 1234.57
print(f"{value:10.2f}") # 宽度10，右对齐 → "   1234.57"
print(f"{value:<10.2f}")# 宽度10，左对齐 → "1234.57   "
ratio=0.456
print(f"{value:.1%}")# 百分比格式 → 45.6%
#这里需要注意百分比格式的%和f是不能共存的
num=42
print(f"{num:05x}") # 十六进制格式 → 00042
```

其有几个特点需要注意:

1.  f-string中可以嵌入任意的Python表达式,包括函数调用,算术运算,条件表达式等,但是尽量不要太复杂,否则会影响代码的可读性.
2.  大括号本身需要转义,可以使用双大括号{{和}}来表示单个大括号.
3.  f-string本身是支持转义字符的,但是在表达式中不支持转义字符.

