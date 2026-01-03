#!/usr/bin/env python3

# report.py

import fileparse
import stock
import tableformatter
from portfolio import Portfolio

def read_portfolio(filename):
    portdict=fileparse.parse_csv(open(filename),select=['name','shares','price'],types=[str,int,float])
    stocks=[stock.stock(d['name'],d['shares'],d['price'])for d in portdict]
    return Portfolio(stocks)

def read_prices(filename):
    return dict(fileparse.parse_csv(open(filename),
                                    types=[str,float],
                                    has_headers=False))

def make_report_data(portfolio,prices):
    '''
    Make a list of (name, shares, price, change) tuples given a portfolio list
    and prices dictionary.
    '''
    rows = []
    for s in portfolio:
        current_price = prices[s.name]
        change = current_price - s.price
        summary = (s.name, s.shares, current_price, change)
        rows.append(summary)
    return rows

def print_report(reportdata,formatter):
    '''
    Print a nicely formated table from a list of (name, shares, price, change) tuples.
    '''
    formatter.headings(['Name','Shares','Price','Change'])
    for name,shares,price,change in reportdata:
        rowdata = [ name, str(shares), f'{price:0.2f}', f'{change:0.2f}' ]
        formatter.row(rowdata)

def portfolio_report(portfoliofile,pricefile,fmt='txt'):        
    '''
    Make a stock report given portfolio and price data files.
    '''
    # Read data files 
    portfolio = read_portfolio(portfoliofile)
    prices = read_prices(pricefile)

    # Create the report data
    report = make_report_data(portfolio, prices)
    # Print it out
    formatter=tableformatter.create_fun(fmt)
    print_report(report,formatter)
def main(argv):
    portfolio_report(argv[0],argv[1],argv[2])

if __name__=='__main__':
    import sys
    if len(sys.argv)==4:
        main(sys.argv[1:])
    else:
        raise Exception('Error')
