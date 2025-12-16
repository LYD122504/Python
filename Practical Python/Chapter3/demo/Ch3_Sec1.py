def square(x):
     return x*x

a=42
b=a+2 # Requires that a is defined

z=square(b) # Requires square and b is defined
print(z)

def foo():
    import math
    print(math.sqrt(2))
    help(math)
    
foo()

def read_prices(filename:str)->dict:
    '''
    Read prices from a CSV file of name, price data
    '''
    prices={}
    with open(filename) as f:
        f_csv=csv.reader(f)
        for row in f_csv:
            prices[row[0]]=float(row[1])
    return prices

print(help(read_prices))
