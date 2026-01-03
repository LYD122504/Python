---
title: Pratical Python-List, File and Functions
date: 2025-09-12 19:12:35
tags:
    - Python
categories: Practical Python
mathjax: true
---

本笔记完全基于David Beazley的Python教程-[Practical Python](https://dabeaz-course.github.io/practical-python/Notes/Contents.html).

## List

列表是Python中存储有序值集合的主要类型,用如下的方式创建:

```python
names=['Elwood','Jake','Curtis']
nums=[39,38,42,65,111]
```

<!--more-->

我们通过input函数接收到的输入是字符串形式,我们可以用字符串的split方法将其转换为列表形式:

```python
text='GOOG,100,490.10'
row=text.split(',')
print(row) # 输出为['GOOG','100','490.10']
```

列表与C语言的数组不同,他允许列表内元素具有不同的数据类型.列表可以通过append方法,在列表末尾加新的元素;列表也可以利用insert方法,在指定索引位置插入新的元素:

```python
names.append('Frank')
print(names)# ['Elwood','Jake','Curtis','Frank']
names.insert(2,'Buster')
print(names)# ['Elwood','Jake','Buster','Curtis','Frank']
names.append(10) 
print(names)# ['Elwood','Jake','Buster','Curtis','Frank',10]
```

列表的其余操作与字符串的操作基本一致,在此我们不再赘述.但是有两个不同需要我们额外指明:列表与字符串不同,他是可以通过索引赋值的方式修改列表内的元素的.

```python
names[1]='Joliet'
print(names) # ['Elwood', 'Joliet', 'Buster', 'Curtis', 'Frank', 10]
```

其次,列表是没有find方法的,如果我们希望在列表中查找某一个元素的索引,只能使用index方法,其如果查找失败返回的是ValueError,而不是find的-1.

因为前面我们提到了列表其实是可以被修改的,故而我们介绍对列表的删除操作.首先,列表自身具有remove方法,我们可以直接利用remove方法来移除我们指定的元素.但是需要注意的是,如果我们指定的元素出现了多次,那么remove方法仅移除第一次出现的;如果我们试图一个不存在的元素,那么他会抛出ValueError异常,因此使用remove方法的时候,尽量保证元素是合法的.除了remove方法以外,python还提供了一个关键字del,del可以直接针对性的删除某个位置的元素或者某段切片的元素.

```python
names.remove('Buster')
print(names)
del names[names.index(10)]
print(names)
s=[0,1,2,3,4,5]
del s[2:5]
print(s)
```

python的删除操作并不会产生列表的空位,而是删除了以后,后续的元素不断前移来填充空位.

Python还提供了列表的排序方法.sort()方法可以在原地修改列表并返回None.

```python
nums.sort()
print(nums)
```

sort方法则提供了两个比较常用的参数:key和reverse.reverse默认是False,也就是默认的排序方式是升序排序,可以通过给他赋值True来完成倒序排序;虽然列表允许其元素具有不同的数据类型,但是sort方法并不能够应用在不同的数据类型,需要用key来指定比较的方式,比较常见的是str,他会将不同的数据类型转换为字符串,并利用字符串的大小比较.

```python
nums.sort(reverse=True)
print(nums)
names.sort()
print(names)
names.append(10)
print(names)
names.sort(key=str)
print(names)
```

sort方法是在原列表的基础上修改,并不会生成新列表.如果希望生成新列表,而不在原列表上修改的话,可以使用sorted函数.

```python
s=sorted(names,key=str,reverse=True)
print(s)
print(names)
```

这里我们需要指出的是列表是不支持数学运算的,因为他的加法被定义为拼接,乘法定义为重复.


<a id="org5172e51"></a>

## File Management

打开文件的语法:

```python
f=open('foo.txt','rt')
```

open接受两个参数,第一个参数就是需要打开的文件位置,第二个参数表示以什么模式打开文件,r表示以只读方式,如果文件不存在,就会报错;w为以只写的方式打开,如果文件不存在,那就会创建一个新文件,如果文件存在就会覆盖原文件内容;a表示追加,并不会覆盖原文件内容,而是在文件的末尾追加内容;r+和w+都表示同时赋予读写权限,但区别在于r+不会覆盖原文件,而遇到文件不存在就会报错;而w+会覆盖原文件,但文件不存在会创建一个文件.rt中的t表示以文本模式读取文件的内容,默认都是文本模式读取,故可以省略;但如果我们希望以二进制方式读取那么就需要自己显式声明,用b表示.

文件读取的语法:

```python
data=f.read(2)
print(data)
data=f.read()
print(data)
```

read方法会一次性读取到文件末尾,而read(n)则是读取n个字符.因此,我们的示例代码的意思是先读取两个字符并输出,然后再从第三个字符开始一直读取到最后再输出.如果我们将这两个读取函数换一下,那么第一次就会返回全部字符,第二次则是返回EOF.

文件的关闭语法:
Python提供了一个手动的close方法,可以自己在程序中手动控制文件的关闭.

```python
f.close()
```

但是在大项目中,同时打开多个文件,文件的关闭检查是一个十分困难的事情.因此python提供了with语句来简化了文件的关闭操作,他会在进入缩进代码块时打开文件,并在离开缩进代码块时自动关闭文件:

```python
with open(filename,'rt') as file:
  statements
```

文件逐行读取的方法:因为read方法他默认了从头读取到尾,如果字符串是多行字符串,我们希望逐行读取,可以利用如下代码实现,

```python
with open(filename,'rt') as file:
  for line in file:
    print(line.strip())
```

文件的写入方法:python提供了一个write方法来为文件写入字符串数据.

```python
with open('outfile','wt') as file:
  out.write('Hello World\n')
```

同时也可以利用输出重定向的方式来实现.

```python
with open('outfile','wt') as out:
  print('Hello World',file=out)
```

## Functions

函数是一系列执行任务并返回结果的语句,需要使用return关键词显式指定函数的返回值.

```python
def fun_name:
  statements
  return return_result
```

函数通过异常来报告错误,异常会导致函数中止;如果异常没有被处理,那么整个程序就会停止.为了调试目的,异常信息会描述发生了什么,错误发生的位置以及一个回溯信息,显示导致失败的其他函数调用.

异常可以被捕捉和处理.捕捉异常可以使用try-except语句,

```python
for line in file:
  fields = line.split(',')
  try:
    shares = int(fields[1])
  except ValueError:
    print("Couldn't parse", line)
```

这里我们用ValueError举例,实际上我们需要与试图捕捉的异常类型相匹配.显然,我们在运行程序时并不知道会发生什么异常,因此异常捕捉一般出现在程序意外崩溃之后才被添加.

同时,我们可以在程序中主动抛出异常,使用raise语句,

```python
raise RuntimeError('What a kerfuffle')
```

这个异常同样会导致程序运行中断,也可以用try-except捕捉:

```python
try:
    raise RuntimeError('What a kerfuffle')
except RuntimeError:
    print("异常处理完成")
```
