# List as a Container
portfolio=[
    ('GOOG',100,490.10),
    ('IBM',50,91.3),
    ('CAT',150,83.44)
]

print(portfolio[0])
print(portfolio[1])

records=[]
records.append(('GooG',100,490.10))
records.append(('IBM', 50, 91.3))
print(records)

record=[]
with open('portfolio.csv','rt') as file:
    next(file)
    for row in file:
        rows=row.split(',')
        record.append((rows[0],int(rows[1]),float(rows[2])))
print(record)

# Dicts as a Container
prices={
    'GOOG': 513.25,
    'CAT':87.27,
    'IBM': 93.37,
    'MSFT': 44.12
}
print(prices)
print(prices['GOOG'])
print(prices['CAT'])

prices={}
prices['GOOG']=513.25
prices['CAT']=87.27
prices['IBM']=93.37
print(prices)

price={}
with open('portfolio.csv','rt') as file:
    next(file)
    for rows in file:
        row=rows.split(',')
        price[row[0]]=float(row[2])
print(price)

if '"AA"' in price:
    print(price['"AA"'])

if 'AB' in price:
    print(price['AA'])
else:
    print('Key is error')

print(prices.get('CAT',0.0))
print(prices.get('CATE',0.0))

holiday={
    (1,3):'New York',
    (5,6):'Wuhan'
}
print(holiday[1,3])
