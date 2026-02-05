# Part1 Number 数字类型
print(3+4*5)
print(23.45/1e-02)
print(7/4)  # 普通除法
print(7//4) # //整数除法
x=1172.5666
# 把数字转换为分数表示
print(x.as_integer_ratio())
a,b=x.as_integer_ratio()
print(a/b)
# 判断数字是否为整数
# 他判断的与类型无关,只要数值上是整数就返回True
print(x.is_integer())
y=4.0
print(y.is_integer())
print(isinstance(y,int))
y=12345
print(y.numerator)
print(y.denominator)
# int 在 Python 中是有理数 p/q 的特例
print(y.bit_length())  # 返回表示该整数所需的最小二进制位数

# Part2 String Manipulation 字符串操作
symbols = 'AAPL IBM MSFT YHOO SCO'
col=[0,1,2,-1,-2]
for i in col:
    print(symbols[i],end=' ')
print()
print(symbols[:4])
print(symbols[-3:])
print(symbols[5:8])
symbols+=' GOOG'
print(symbols)
symbols='HPQ '+symbols
print(symbols)
print('IBM' in symbols)
print('AA' in symbols)
print('CAT' in symbols)
print(symbols.lower())
lowersyms=symbols.lower()
print(lowersyms)
index=symbols.find('MSFT')
print(index)
print(symbols[index:index+len('MSFT')])
symbols=symbols.replace('SCO',' ')
print(symbols)

# Part3 List Manipulation
# 不写参数时,自动处理任意数量的空白字符,不会产生空字符串
# 如果加入参数,则按参数进行分割
symlist=symbols.split()
print(symlist)
for i in col:
    print(symlist[i],end=' ')
print()
symlist[2]='AIG'
print(symlist)
for s in symlist:
    # sep='' 表示不加任何分隔符
    print('s=',s,sep='')
print('AIG' in symlist)
print('CAT' in symlist)
symlist.append('RHT')
print(symlist)
symlist.insert(1,'AA')
print(symlist)
symlist.remove('MSFT')
print(symlist)
print(symlist.index('YHOO'))
print(symlist[symlist.index('YHOO')])
symlist.sort()
print(symlist)
symlist.sort(reverse=True)
print(symlist)
nums=[101,102,103]
items=[symlist,nums]
print(items)
print(items[0])
print(items[0][1])
print(items[0][1][2])
print(items[1])
print(items[1][1])

# Part4 Dictionaries 字典
prices={'IBM':91.1,'GOOG':490.1,'AAPL':312.23}
print(prices)
print(prices['IBM'])
prices['IBM']=123.45
print(prices)
prices['HPQ']=26.15
print(prices)
dic_key=list(prices)
print(dic_key)
del prices['AAPL']
print(prices)