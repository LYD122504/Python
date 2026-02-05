class Stock:
    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price
    def cost(self):
        return self.shares * self.price
if __name__ == "__main__":
    s=Stock('GOOG',100,490.1)
    print(s.name)
    print(s.shares)
    print(s.price)
    print(s.cost())
    print('%10s %10d %10.2f' % (s.name, s.shares, s.price))
    t=Stock('IBM',50,91.5)
    print(t.cost())