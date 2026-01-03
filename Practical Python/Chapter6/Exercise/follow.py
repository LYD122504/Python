import os
import time
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

if __name__=='__main__':
    import report

    portfolio = report.read_portfolio('../data/portfolio.csv')

    for line in follow('stocklog.csv'):
        row = line.split(',')
        name = row[0].strip('"')
        price = float(row[1])
        change = float(row[4])
        if name in portfolio:
            print(f'{name:>10s} {price:>10.2f} {change:>10.2f}')