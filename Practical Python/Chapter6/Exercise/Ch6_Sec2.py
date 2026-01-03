import csv
import os # 提供与操作系统交互的功能,处理文件指针的移动
import time # 提供时间相关功能,这里用来让循环暂停一段时间,避免CPU空转
# Exercise 6.4: A Simple Generator
def filematch(filename,substr):
    with open(filename,'r') as f:
        for line in f:
            if substr in line:
                yield line.strip()


for line in open("../data/portfolio.csv"):
    print(line.strip())
for line in filematch('../data/portfolio.csv', 'IBM'):
        print(line)
'''
f = open('stocklog.csv')#读取一个stocklog.csv文件返回一个文件对象
#offset=0表示移动0个字节,whence=os.SEEK_END,表示从文件末尾开始移动
f.seek(0, os.SEEK_END)   # Move file pointer 0 bytes from end of file
#把指针移动到文件末尾,只处理文件后续新增的内容,类似于tail -f
while True:
    #从文件当前位置读取一行文本
    line = f.readline()
    if line == '':
        # 避免无限循环空转消耗 CPU;模拟等待新数据的行为
        time.sleep(0.1)   # Sleep briefly and retry
        continue
    fields = line.split(',')
    name = fields[0].strip('"')
    price = float(fields[1])
    change = float(fields[4])
    if change < 0:
        print(f'{name:>10s} {price:>10.2f} {change:>10.2f}')'''

# Exercise 6.6: Using a generator to produce data
def follow(filename):
    f = open(filename)#读取一个stocklog.csv文件返回一个文件对象
    #offset=0表示移动0个字节,whence=os.SEEK_END,表示从文件末尾开始移动
    f.seek(0, os.SEEK_END)   # Move file pointer 0 bytes from end of file
    #把指针移动到文件末尾,只处理文件后续新增的内容,类似于tail -f
    while True:
        #从文件当前位置读取一行文本
        line = f.readline()
        if line == '':
        # 避免无限循环空转消耗 CPU;模拟等待新数据的行为
            time.sleep(0.1)   # Sleep briefly and retry
            continue
        yield line
if __name__ == '__main__':
    for line in follow('stocklog.csv'):
        fields = line.split(',')
        name = fields[0].strip('"')
        price = float(fields[1])
        change = float(fields[4])
        if change < 0:
            print(f'{name:>10s} {price:>10.2f} {change:>10.2f}')