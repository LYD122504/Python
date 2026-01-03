---
title: Pratical Python-Regular expression
date: 2025-09-07 15:52:35
tags:
    - Python
categories: Practical Python
mathjax: true
---

## Regular Expression

在上一节中提到了Python可以利用字符串的find和index方法来查找字符串,但是这种方法只能查找固定的字符串,也就是精确查找.而我们在正常使用过程中模糊查找其实更为常见,例如查找所有以a开头,以b结尾的字符串,这就需要利用正则表达式来实现搜索.

正则表达式的基本语法如下:

<!--more-->

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">



<colgroup>
<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">符号</th>
<th scope="col" class="org-left">含义</th>
<th scope="col" class="org-left">示例</th>
</tr>
</thead>

<tbody>
<tr>
<td class="org-left">.</td>
<td class="org-left">匹配除换行符外的任意单个字符</td>
<td class="org-left">a.b匹配开头为a,结尾为b的连续三个字符</td>
</tr>


<tr>
<td class="org-left">\^</td>
<td class="org-left">匹配字符串的开头</td>
<td class="org-left">^abc匹配以abc开头的字符串</td>
</tr>


<tr>
<td class="org-left">\$</td>
<td class="org-left">匹配字符串的结尾</td>
<td class="org-left">$abc匹配以abc结尾的字符串</td>
</tr>


<tr>
<td class="org-left">[]</td>
<td class="org-left">定义字符集合,匹配其中任意一个字符</td>
<td class="org-left">[aeiou]匹配任意一个原因字母</td>
</tr>


<tr>
<td class="org-left">[^]</td>
<td class="org-left">定义字符集合,匹配不在其中任意的一个字符</td>
<td class="org-left">[^0-9]匹配任意非数字字符</td>
</tr>


<tr>
<td class="org-left">-</td>
<td class="org-left">字符类中表示范围</td>
<td class="org-left">[a-z]匹配任意小写字母</td>
</tr>


<tr>
<td class="org-left">\*</td>
<td class="org-left">匹配前面的子表达式零次或多次</td>
<td class="org-left">a*e匹配开头有且仅有0个或多个a,结尾为e的字符</td>
</tr>


<tr>
<td class="org-left">+</td>
<td class="org-left">匹配前面的子表达式一次或多次</td>
<td class="org-left">a+e匹配开头有且仅有1个或多个a,结尾为e的字符</td>
</tr>


<tr>
<td class="org-left">?</td>
<td class="org-left">匹配前面的子表达式零次或者一次</td>
<td class="org-left">colou?r匹配color和colour</td>
</tr>


<tr>
<td class="org-left">{n}</td>
<td class="org-left">精确匹配前面的子表达式n次</td>
<td class="org-left">da{3}e匹配daaae</td>
</tr>


<tr>
<td class="org-left">{n,}</td>
<td class="org-left">至少匹配前面的子表达式n次</td>
<td class="org-left">da{2,}e匹配daae,daaae等</td>
</tr>


<tr>
<td class="org-left">{n,m}</td>
<td class="org-left">匹配前面的子表达式n次到m次</td>
<td class="org-left">a{2,4}匹配aa,aaa,aaaa</td>
</tr>


<tr>
<td class="org-left">()</td>
<td class="org-left">定义子表达式或捕获组</td>
<td class="org-left">(ab)+匹配ab,abab等</td>
</tr>
</tbody>
</table>

正则表达式里的特殊字符如果需要作为普通字符使用,则需要在其前面加上反斜杠\\进行转义,如:

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">



<colgroup>
<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">符号</th>
<th scope="col" class="org-left">含义</th>
<th scope="col" class="org-left">等价符号</th>
</tr>
</thead>

<tbody>
<tr>
<td class="org-left">\​d</td>
<td class="org-left">匹配任意数字</td>
<td class="org-left">等价于[0-9]</td>
</tr>


<tr>
<td class="org-left">\​D</td>
<td class="org-left">匹配任意非数字</td>
<td class="org-left">等价于[^0-9]</td>
</tr>


<tr>
<td class="org-left">\​w</td>
<td class="org-left">匹配任意单词字符(字母,数字,下划线)</td>
<td class="org-left">[a-zA-Z0-9_]</td>
</tr>


<tr>
<td class="org-left">\​W</td>
<td class="org-left">匹配任意非单词字符(字母,数字,下划线)</td>
<td class="org-left">[^a-zA-Z0-9_]</td>
</tr>


<tr>
<td class="org-left">\​s</td>
<td class="org-left">匹配任意空白字符(空格,制表符,换行符)</td>
<td class="org-left">[ \​t\​n]</td>
</tr>

<tr>
<td class="org-left">\​S</td>
<td class="org-left">匹配任意非空白字符(空格,制表符,换行符)</td>
<td class="org-left">[^ \​t \​n]</td>
</tr>


<tr>
<td class="org-left">\​b</td>
<td class="org-left">边界匹配符,如果在左边出现要求是开头,右边则是结尾,同时出现则精确匹配</td>
<td class="org-left">^,$,""</td>
</tr>
</tbody>
</table>

这里我们对前面提到的正则表达式的基本语法进行一些补充说明:

1.  \*,+,?和{n,m}这些量词都是贪婪的也就是他会尽可能多的匹配字符,如下:

    ```python
    import re
    text="<div>abc</div><div>def</div>"
    re.findall(r"<div>.*</div>",text) # ['<div>abc</div><div>def</div>']
    ```

    这里的.\*会尽可能多的匹配字符,直到最后一个</div>为止.如果想让其变为非贪婪模式,则可以在量词后面加上?,如下:

    ```python
    # 非贪婪模式
    re.findall(r"<div>.*?</div>", text)
    # 结果: ['<div>abc</div>', '<div>def</div>']
    ```

2.  匹配开头或者结尾的时候只写了部分模式,这并不会匹配整个字符串,而是匹配字符串的开头或者结尾部分,如下:

    ```python
    re.findall(r"^abc", "abcdef") # ['abc']
    re.findall(r"def$", "abcdef") # ['def']
    ```

3.  忘记了对特殊字符做转义

    ```python
    re.findall(r"d{3}.txt","dddktxt") # ['dddktxt']
    ```

4.  字符集和字符分组混用错误:[abc]可以匹配单个字符'a','b'和'c';而(abc)匹配整个字符串"abc".

re模块是Python标准库中用于正则表达式操作的模块,提供查找,匹配,替换,分组等功能.re模块的基本函数为

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">



<colgroup>
<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">函数</th>
<th scope="col" class="org-left">作用</th>
</tr>
</thead>

<tbody>
<tr>
<td class="org-left">re.match(pattern,string)</td>
<td class="org-left">从字符串开头匹配</td>
</tr>


<tr>
<td class="org-left">re.search(pattern,string)</td>
<td class="org-left">搜索整个字符串,找到第一个匹配</td>
</tr>


<tr>
<td class="org-left">re.findall(pattern,string)</td>
<td class="org-left">返回所有匹配的字符串列表</td>
</tr>


<tr>
<td class="org-left">re.finditer(pattern,string)</td>
<td class="org-left">返回迭代器,每个元素是Match对象</td>
</tr>


<tr>
<td class="org-left">re.fullmatch(pattern,string)</td>
<td class="org-left">整个字符串必须完全匹配</td>
</tr>


<tr>
<td class="org-left">re.split(pattern,string)</td>
<td class="org-left">按模式分割字符串</td>
</tr>


<tr>
<td class="org-left">re.sub(pattern,repl,string)</td>
<td class="org-left">替换匹配的部分</td>
</tr>


<tr>
<td class="org-left">re.subn(pattern,repl,string)</td>
<td class="org-left">返回(替换后字符串,替换次数)</td>
</tr>
</tbody>
</table>

返回的match对象的常用属性:

```python
import re
m=re.search(r"\d+","abc123def")
print(m.group()) # 返回匹配的字符串"123"
print(m.start()) # 返回匹配子串的起始索引,3
print(m.end()) # 返回匹配子串的结束索引,6
print(m.span()) # 返回(start,end),(3,6)
```

re模块提供了一个编译模式,可以提高后续使用相同的正则表达式的运行效率.re.compile的作用会将一个正则表达式编译成一个正则对象,后续可以重复使用这个对象来匹配字符串.这样的好处是

1.  复用性强,不需要每次都写pattern,直接使用正则对象的方法.
2.  效率更高,编译过的正则对象会缓存,特别是同一个模式需要多次匹配时,具有更高的性能

其基本语法为:

```python
import re
# re.compile的基本语法;pattern为正则表达式字符串,flags则是表示匹配模式
regex=re.compile(pattern,flags=0)
pattern=re.compile(r"\d+")
text="Order123, Item456, Code789"
print(pattern.findall(text))
for m in pattern.finditer(text):
    print(m.group(),m.span())
```

上面提到了re.compile的标准语法中存在一个flags变量,实际上re的每个函数都有这个变量,在此介绍flags变量的值及其作用:

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">



<colgroup>
<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">FLAGS</th>
<th scope="col" class="org-left">作用</th>
</tr>
</thead>

<tbody>
<tr>
<td class="org-left">re.I(re.IGNORECASE)</td>
<td class="org-left">忽略大小写,匹配时不区分大小写</td>
</tr>


<tr>
<td class="org-left">re.M(re.MULTILINE)</td>
<td class="org-left">让^和$作用于每一行的开头和结尾,默认仅匹配整个字符串的开头结尾</td>
</tr>


<tr>
<td class="org-left">re.S(re.DOTALL)</td>
<td class="org-left">默认.不匹配换行,开启后可以匹配换行</td>
</tr>


<tr>
<td class="org-left">re.X(re.VERBOSE)</td>
<td class="org-left">正则里可以加空格和注释，提高可读性</td>
</tr>
</tbody>
</table>

