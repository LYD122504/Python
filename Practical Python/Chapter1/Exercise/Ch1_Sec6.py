# File Preliminaries
with open('portfolio.csv','rt') as file:
    data=file.read()
    print(data)

with open('portfolio.csv','rt') as file:
    for line in file:
        print(line,end=' ')

# 手动读取单行文本
f = open('portfolio.csv','rt')
# next函数就是返回文件的下一行文本.如果反复调用可以得到连续的行
header=next(f)
print(header,end=' ')
# 这里的for循环其实就是在不断调用next
for line in f:
    print(line,end=' ')
f.close()

# 读单行后的操作
f=open('portfolio.csv','rt')
headers=next(f)
print(headers)
for line in f:
    row=line.split(',')
    print(row)
f.close()

#  Reading a data file
sum=0.0
with open('portfolio.csv','rt') as file:
    headers=next(file)
    for line in file:
        row=line.split(',')
        sum+=int(row[1])*float(row[2])
print('Total market value: $',sum)

# 压缩文件读取
import gzip
# 值得注意的是,这里的模式需要显式提供t,否则会以二进制模式读取
with gzip.open('portfolio.csv.gz','rt') as file:
    for line in file:
        print(line,end=' ')