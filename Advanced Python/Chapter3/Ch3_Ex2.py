import stock
import tableformat
s=stock.Stock('ACME',50,91.1)
print(s.shares)
s.date='10/31/2017'
print(s.date)
print(s.cost)
print(stock.Stock.cost)
attributes=['name','shares','price']
for attr in attributes:
    print(attr, '=', getattr(s, attr))

# The Three Operations
s=stock.Stock('GOOG',100,490.1)
print(getattr(s,'name'))
setattr(s,'shares',50)
print(s.shares)
delattr(s,'shares')
print(hasattr(s,'name'))
print(hasattr(s,'blah'))

# Using getattr()
s=stock.Stock('GOOG',100,490.1)
field=['name','shares','price']
for name in field:
    print(name,getattr(s,name))

portfolio=stock.read_portfolio('../Data/portfolio.csv')
tableformat.print_table(portfolio,['name','shares','price'])
tableformat.print_table(portfolio,['shares','name'])

# Bound Methods
print(s.cost)
print(s.cost())
print(getattr(s,'cost'))
print(getattr(s,'cost')())
c=s.cost
print(c())
s.shares=75
print(c())
print(c.__self__)
print(c.__func__)
print(c.__func__(c.__self__))