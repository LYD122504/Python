from typedproperty import String, Integer, Float, typedproperty
class stock:
    name=String('name')
    price=Float('price')
    shares=Integer('shares')
    def __init__(self,name,shares,price):
        self.name=name
        self.shares=shares
        self.price=price
    @property
    def cost(self):
        return self.shares*self.price
    def sell(self,shares):
        self.shares-=shares
        return self.shares
    def __repr__(self):
        return f'Stock("{self.name}",{self.shares},{self.price})'
    
if __name__=='__main__':
    s = stock('GOOG', 100, 490.1)
    print(s.cost)
    print(s.__dict__)
    columns = ['name', 'shares']
    for colname in columns:
        print(colname, '=', getattr(s, colname))