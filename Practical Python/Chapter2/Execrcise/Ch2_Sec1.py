import csv
f=open('portfolio.csv','rt')
rows=csv.reader(f)
header=next(rows)
print(header)

# Tuples 元组
row=next(rows)
t=(row[0],int(row[1]),float(row[2]))
print(t)
cost=t[1]*t[2]
print(cost)
print(f'{cost:.2f}')

tnew=(t[0],75,t[2])
print(tnew)

name,share,prices=t
print(name,share,prices)
tnew=name,share*0.1,prices
print(tnew)

# Dictonaries 字典
d={
    'name': row[0],
    'shares':int(row[1]),
    'price':float(row[2])
}
print(d)
cost=d['shares']*d['price']
print(cost)

d['shares']=75
print(d)
cost=d['shares']*d['price']
print(cost)

d['date']=(6,11,2007)
d['account']=12345
print(d)

# Additional dictonary operation
l=list(d) # 利用list()函数可以将字典的所有键提取成一个列表
print(l)

for k in d:
    print('k=',k)

for k in d:
    print('keys=',k,'values=',d[k])

keys=d.keys()
print(keys)

del d['account']
print(keys)
items=d.items()
print(items)
for k,v in items:
    print(k,'=',v)
d1=dict(items)
print(d1)
f.close()
