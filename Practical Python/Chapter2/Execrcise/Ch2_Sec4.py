import csv
# Exercise 2.13 Counting
for n in range(10):
    if n==9:
        print(n)
        continue
    print(n,end=' ')
for n in range(10,0,-1):
    if n==1:
        print(n)
        continue
    print(n,end=' ')
for n in range(0,10,2):
    if n==8:
        print(n)
        continue
    print(n,end=' ')

# Exercise 2.14 More sequence operations
data=[4,9,1,25,16,100,49]
print("Min:",min(data))
print("Max:",max(data))
print("Sum:",sum(data))

for x in data:
    print(x,end=' ')
for n,x in enumerate(data):
    print(f"Index {n}: {x}")

# Exercise 2.15 A practical enumerate() example
def portfolio_cost_v2(filename):
    sum=0.0
    with open(filename,'rt') as file:
        headers=next(file)
        for lineno,line in enumerate(file,1):
            row=line.split(',')
            try:
                sum+=int(row[1])*float(row[2])
            except ValueError:
                # 第一个strip()去掉行尾的换行符，第二个split(',')重新分割
                line=line.strip().split(',')
                print(f"Raw {lineno}: Couldn't convert: {line}")
    return sum

cost=portfolio_cost_v2('missing.csv')
print('Total market value: $',cost)

# Exercise 2.16: Using the zip() function
f=open('portfolio.csv','rt')
rows=csv.reader(f)
headers=next(rows)
print(headers)
row=next(rows)
print(row)
print(list(zip(headers,row)))
print(dict(zip(headers,row)))
f.close()

def portfolio_cost_v3(filename):
    sum=0.0
    f=open(filename,'rt')
    rows=csv.reader(f)
    headers=next(rows)
    for lineno,row in enumerate(rows,start=1):
        record=dict(zip(headers,row))
        try:
            sum+=int(record['shares'])*float(record['price'])
        except ValueError:
            print(f"Raw {lineno}: Couldn't convert: {row}")
    f.close()
    return sum
cost=portfolio_cost_v3('portfoliodate.csv')
print('Total market value: $',cost)

# Exercise 2.17: Inverting a dictionary
prices = {
        'GOOG' : 490.1,
        'AA' : 23.45,
        'IBM' : 91.1,
        'MSFT' : 34.23
}
print(prices.items())
pricelist=list(zip(prices.keys(),prices.values()))
print(pricelist)
print(min(pricelist))
print(max(pricelist))
print(sorted(pricelist))# sorted()函数返回一个新的列表，并不改变原来的列表
