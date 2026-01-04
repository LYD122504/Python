# pcost.py

from . import report

def portfolio_cost(filename):
    '''
    Computes the total cost (shares*price) of a portfolio file
    '''
    portfolio = report.read_portfolio(filename)
    return portfolio.total_cost
if __name__=='__main__':
    import sys
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    else:
        filename = input('Enter a filename:')

    cost = portfolio_cost(filename)
    print('Total cost:', cost)