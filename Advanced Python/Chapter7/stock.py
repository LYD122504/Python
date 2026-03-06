from structure import Structure, validate_attributes
import sys
import validate
class Stock(Structure):
    _fields=('name','shares','price')
    name = String()
    shares = PositiveInteger()
    price = PositiveFloat()
    def __eq__(self,other):
        return isinstance(other,Stock) and (self.name,self.shares,self.price)==(other.name,other.shares,other.price)
    @property
    def cost(self):
        return self.shares * self.price
    def sell(self, nshares: PositiveInteger):
        self.shares -= nshares
