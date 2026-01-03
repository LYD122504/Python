class stock:
    __slots__=('name','_shares','price')
    def __init__(self,name,shares,price):
        self.name=name
        self.shares=shares
        self.price=price
    @property
    def cost(self):
        return self.shares*self.price
    @property
    def shares(self):
        return self._shares
    @shares.setter
    def shares(self,value):
        if not isinstance(value, int):
            raise TypeError('Expected int')
        self._shares = value
    def sell(self,shares):
        self.shares-=shares
        return self.shares
    def __repr__(self):
        return f'Stock("{self.name}",{self.shares},{self.price})'
    
if __name__=='__main__':
    s = stock('GOOG', 100, 490.1)
    print(s.cost)
    print(s.name)
    s.blah=42
    columns = ['name', 'shares']
    for colname in columns:
        print(colname, '=', getattr(s, colname))