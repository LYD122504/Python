symbols = 'HPQ,AAPL,IBM,MSFT,YHOO,DOA,GOOG'
symlist=symbols.split(',')
print(symlist)

# Exercise 1.19: Extracting and reassigning list elements
print(symlist[0])
print(symlist[-1])
print(symlist[2])
symlist[2]='AIG'
print(symlist)
print(symlist[0:3])
print(symlist[-2:])
mysyms=[]
mysyms.append('GOOG')
print(mysyms)
# 列表切片的赋值要求右端必须是可迭代对象,至于迭代对象的长度是否与切片长度相等则无所谓,系统会自动调整列表长度
symlist[-2:]=mysyms
print(symlist)

# Exercise 1.20: Looping over list items
for s in symlist:
    print('s=',s)

# Exercise 1.21: Membership tests
if 'AIG' in symlist:
    print('AIG is in the list')
else:
    print('AIG is not in the list')

# Exercise 1.22: Appending, inserting, and deleting items
symlist.append('RHT')
print(symlist)
symlist.insert(1,'AA')
print(symlist)
symlist.remove('MSFT')
print(symlist)
symlist.append('YHOO')
print(symlist)
print(symlist.index('YHOO'))
print(symlist[symlist.index('YHOO')])
print(symlist.count('YHOO'))
del symlist[symlist.index('YHOO')]
print(symlist)

# Exercise 1.23: Sorting
symlist.sort()
print(symlist)
symlist.sort(reverse=True)
print(symlist)

# Exercise 1.24: Putting it all back together
# s.join(list)  以字符串s作为分隔符,将字符列表的所有元素连接成一个新的字符串;要求list必须是字符串列表
a=','.join(symlist)
print(a)
b=':'.join(symlist)
print(b)
c=' '.join(symlist)
print(c)

# Exercise 1.25: Lists of anything
nums=[101,102,103]
items=['spam',symlist,nums]
print(items)
print(items[0])
print(items[0][0])
print(items[1])
print(items[1][1])
print(items[1][1][1])