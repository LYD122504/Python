# 4.1 Objects as Data Structures
import stock
a=stock.stock('GOOG',100,490.10)
print(a.name,a.shares,a.price)
b = stock.stock('AAPL', 50, 122.34)
c = stock.stock('IBM', 75, 91.75)
print(b.shares*b.price)
print(c.shares*c.price)
stocks=[a,b,c]
print(stocks)
for s in stocks:
    print(f'{s.name:>10s} {s.shares:>10d} {s.price:>10.2f}')

# 4.2 Adding some Methods
s=stock.stock('GOOG',100,490.10)
print(s.cost())
print(s.shares)
print(s.sell(25))
print(s.cost())

# 4.3 Creating a list of instances
import fileparse
with open('./data/portfolio.csv') as lines:
    portdict=fileparse.parse_csv(lines,select=['name','shares','price'],types=[str,int,float])
portfolio=[stock.stock(d['name'],d['shares'],d['price'])for d in portdict]
print(portfolio)
print(sum([s.cost() for s in portfolio]))