# readport.py
import csv
def read_portfolio(filename):
    portfolio=[]
    with open(filename) as f:
        rows=csv.reader(f)
        headers=next(rows)
        for row in rows:
            record={
                'name': row[0],
                'shares': int(row[1]),
                'price': float(row[2])
            }
            portfolio.append(record)
    return portfolio
if __name__ == '__main__':
    portfolio=read_portfolio('../Data/portfolio.csv')
    from pprint import pprint
    pprint(portfolio)
    # Find all holdings more than 100 shares
    filter_list=[s for s in portfolio if s['shares']>100]
    pprint(filter_list)
    # Compute total cost(shares*prices)
    total_cost=sum([s['shares']*s['price'] for s in portfolio])
    print('Total cost:',total_cost)
    # Find all unique stock names
    filter_set={s['name'] for s in portfolio}
    pprint(filter_set)
    # Count the total shares of each of stock
    dict_name={s['name']:0 for s in portfolio}
    for s in portfolio:
        dict_name[s['name']]+=s['shares']
    pprint(dict_name)

    from collections import Counter
    totals=Counter()
    for s in portfolio:
        totals[s['name']]+=s['shares']
    pprint(totals)
    # Get the two most common holdings
    print(totals.most_common(2))
    # Adding counters together
    more = Counter()
    more['IBM'] = 75
    more['AA'] = 200
    more['ACME'] = 30
    print(more)
    print(totals + more)
    from collections import defaultdict
    byname=defaultdict(list)
    for s in portfolio:
        byname[s['name']].append(s)
    pprint(byname['IBM'])