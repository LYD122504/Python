names=['Elwood','Jake','Curtis']
nums=[39,38,42,65,111]

text='GOOG,100,490.10'
row=text.split(',')
print(row)

print(names)
names.append('Frank')
print(names)
names.insert(2,'Buster')
print(names)
names.append(10)
print(names)

print(f"names:{names}, nums:{nums}")
print(names+nums)

print(names[0])
print(names[1])
print(names[0:2])
print(names[-1])
print(names[-2])

# 这与字符串有所不同,字符串不支持项的赋值
names[1]='Joliet'
print(names)

print('Elwood' in names)       # True
print('Britney' not in names)  # True

s=[1,2,4]
print(s*2)

for name in names:
    print(name)

names.remove('Buster')
print(names)
del names[names.index(10)]
print(names)

nums.sort()
print(nums)
nums.sort(reverse=True)
print(nums)
names.sort()
print(names)

names.append(10)
print(names)
names.sort(key=str)
print(names)

s=sorted(names,key=str,reverse=True)
print(s)
print(names)