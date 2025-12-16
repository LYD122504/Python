import csv
f=open('portfolio.csv')
rows=csv.reader(f)
headers=next(rows)
types=[str,int,float]
row=next(rows)
print(row)
print(types[0](row[0]))
print(list(zip(types,row)))
converted = [func(val) for func,val in zip(types,row)]
print(converted)

print(dict(zip(headers,converted)))
d={name: func(val) for name,func,val in zip(headers,types,row)}
print(d)
f.close()

f=open('dowstocks.csv')
rows=csv.reader(f)
header=next(rows)
print(header)
row=next(rows)
print(row)
types=[str,float,str,str,float,float,float,float,int]
converted=[func(val) for func,val in zip(types,row)]
print(converted)
record=dict(zip(header,converted))
print(record)

l=record['date'].split('/')
print(l)
record['date']=tuple([int(item) for item in l])
print(record['date'])