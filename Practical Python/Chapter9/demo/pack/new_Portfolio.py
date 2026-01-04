from . import stock
from . import fileparse
class Portfolio:
    def __init__(self):
        self.holdings = []
    def append(self,holding):
        if not isinstance(holding,stock.stock):
            raise TypeError('Can only append stock instances')
        self.holdings.append(holding)
    @classmethod
    def from_csv(cls,lines,**opt):
        self=cls()
        portdict=fileparse.parse_csv(lines,select=['name','shares','price'],types=[str,int,float],**opt)
        self.holdings=[stock.stock(**d)for d in portdict]
        return self
if __name__=='__main__':
    with open('../data/portfolio.csv') as lines:
        port = Portfolio.from_csv(lines)
    for s in port.holdings:
        print(s)