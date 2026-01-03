from pprint import pprint
# List Sorting
s=[10,1,7,3]
print(s)
s.sort()
print(s)
s=[10,1,7,3]
print(s)
s.sort(reverse=True)
print(s)
portfolio=[{'name': 'AA', 'price': 32.2, 'shares': 100},
{'name': 'IBM', 'price': 91.1, 'shares': 50},
{'name': 'CAT', 'price': 83.44, 'shares': 150},
{'name': 'MSFT', 'price': 51.23, 'shares': 200},
{'name': 'GE', 'price': 40.37, 'shares': 95},
{'name': 'MSFT', 'price': 65.1, 'shares': 50},
{'name': 'IBM', 'price': 70.44, 'shares': 100}]
def stock_name(s):
    return s['name']
portfolio.sort(key=stock_name)
pprint(portfolio)
portfolio=[{'name': 'AA', 'price': 32.2, 'shares': 100},
{'name': 'IBM', 'price': 91.1, 'shares': 50},
{'name': 'CAT', 'price': 83.44, 'shares': 150},
{'name': 'MSFT', 'price': 51.23, 'shares': 200},
{'name': 'GE', 'price': 40.37, 'shares': 95},
{'name': 'MSFT', 'price': 65.1, 'shares': 50},
{'name': 'IBM', 'price': 70.44, 'shares': 100}]
def stock_name(s):
    return s['name']
portfolio.sort(key=lambda s:s['name'])
pprint(portfolio)