# List Comprehensions
nums=[1,2,3,4]
squares=[x*x for x in nums]
print(squares)
twice=[2*x for x in nums if x>2]
print(twice)

# Sequence Reductions
import csv
def read_dic(filename):
    d_list=[]
    with open(filename,'rt') as f:
        rows=csv.reader(f)
        header=next(rows)
        for row in rows:
            dtemp={}
            dtemp['name']=row[0]
            dtemp['share']=int(row[1])
            dtemp['price']=float(row[2])
            d_list.append(dtemp)
    return d_list
portfolio=read_dic(r'./portfolio.csv')
cost=sum(item['share'] * item['price'] for item in portfolio)
print(cost)

# Data Queries
more100=[s for s in portfolio if s['share']>100]
print(more100)
msftibm=[s for s in portfolio if s['name'] in ('MSFT','IBM')]
print(msftibm)
cost10k = [ s for s in portfolio if s['share'] * s['price'] > 10000 ]
print(cost10k)

# Data Extraction
name_shares=[(s['name'],s['share']) for s in portfolio]
print(name_shares)
names={s['name'] for s in portfolio}
print(names)
holdings={name:0 for name in names}
for s in portfolio:
    holdings[s['name']]+=s['share']
print(holdings)

# Extracting Data From CSV Files
# 从CSV文件中提取一行标题信息
import csv
f=open(r'./portfolio.csv','rt')
rows=csv.reader(f)
header=next(rows)
print(header)
# 定义一个关心列的列表
select=['name','share','price']
# 提取关心列的索引
indices=[header.index(col) for col in select]
print(indices)
# 提取关心列的数据并用字典组合
row=next(rows)
# 这里其实是把关心的列名和对应的索引组合成一个zip对象,在zip对象上迭代
record={col:row[index] for col,index in zip(select,indices)}