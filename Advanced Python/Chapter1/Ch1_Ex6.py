import pcost
from stock import Stock
pcost.portfolio_cost('../Data/portfolio2.dat')
s=Stock('GOOG',100,490.1)
print(s.name)
print(s.cost())