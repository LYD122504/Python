class stock:
    def __init__(self,name,shares,price):
        self.name=name
        self.shares=shares
        self.price=price
    def cost(self):
        return self.shares*self.price
    def sell(self,shares):
        self.shares-=shares
        return self.shares
    def __repr__(self):
        return f'Stock("{self.name}",{self.shares},{self.price})'
    
if __name__=='__main__':
    s = stock('GOOG', 100, 490.1)
    columns = ['name', 'shares']
    for colname in columns:
        print(colname, '=', getattr(s, colname))