import stock
class MyStock(stock.Stock):
    def __init__(self,name,shares,price,factor):
        super().__init__(name,shares,price)
        self.factor=factor
    def panic(self):
        self.sell(self.shares)
    def cost(self):
        return self.factor * super().cost
s=MyStock('GOOG',100,490.10,1.25)
print(s.cost())
s.sell(25)
print(s.shares)
s.panic()
print(s.shares)
print(isinstance(s,stock.Stock))

# Print Table
import reader
import tableformat
portfolio=reader.read_csv_as_instances('../Data/portfolio.csv',stock.Stock)
formatter=tableformat.TextTableFormatter()
tableformat.print_table(portfolio,['name','shares','price'],formatter)
print()
formatter=tableformat.CSVTableFormatter()
tableformat.print_table(portfolio,['name','shares','price'],formatter)
print()
formatter=tableformat.HTMLTableFormatter()
tableformat.print_table(portfolio,['name','shares','price'],formatter)
print()
formatter=tableformat.create_formatter('text')
tableformat.print_table(portfolio,['name','shares','price'],formatter)
