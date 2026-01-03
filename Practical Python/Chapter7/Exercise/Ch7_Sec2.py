import report
portfolio=list(report.read_portfolio('../data/portfolio.csv'))
for s in portfolio:
    print(s)
def stock_name(s):
    return s.name
portfolio.sort(key=lambda s:s.name)
for s in portfolio:
    print(s)
#portfolio.sort(key=stock_name)
#for s in portfolio:   
    #print(s)
