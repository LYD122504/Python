def greeting(name):
    'Issues a greeting'
    print("Hello",name)
greeting("World")

def portfolio_cost(filename):
    sum=0.0
    with open(filename,'rt') as file:
        headers=next(file)
        for line in file:
            row=line.split(',')
            try:
                sum+=int(row[1])*float(row[2])
            except ValueError:
                print('Missing data for',row[0])
    return sum

cost=portfolio_cost('portfolio.csv')
print('Total market value: $',cost)


cost=portfolio_cost('missing.csv')
print('Total market value: $',cost)

import csv
f=open('portfolio.csv','rt')
rows=csv.reader(f)
headers=next(rows)
for row in rows:
    print(row)
f.close()
# csv可以处理一下低级细节如引号和逗号分隔

def portfolio_cost_v2(filename):
    sum=0.0
    f=open('portfolio')
    with open(filename,'rt') as file:
        headers=next(file)
        for line in file:
            row=line.split(',')
            try:
                sum+=int(row[1])*float(row[2])
            except ValueError:
                print('Missing data for',row[0])
    return sum

cost=portfolio_cost_v2('portfolio.csv')
print('Total market value: $',cost)