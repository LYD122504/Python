# Exe 6.1 Iteration Illustrated
a=[1,9,4,25,16]
i=a.__iter__()
print(i)
for j in range(len(a)):
    print(i.__next__())
# print(i.__next__())
f=open('../data/portfolio.csv')
fiter=f.__iter__()
for i in fiter:
    print(i)

# Exercise 6.3: Making a more proper container
import report
portfolio=report.read_portfolio('../data/portfolio.csv')
print(len(portfolio))
print(portfolio[0])
print(portfolio[1])
print(portfolio[0:3])
print('IBM' in portfolio)
print('AAPL' in portfolio)