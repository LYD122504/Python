def portfolio_cost(filepath):
    sum=0.0
    with open(filepath,'r') as f:
        for line in f:
            linelist=line.split()
            try:
                shares=int(linelist[1])
                price=float(linelist[2])
                sum+=shares*price
            except ValueError as e:
                print(f'Could not convert data: {repr(line)}')
                print(e)
    print(f'Total cost: {sum}')
if __name__ == '__main__':
    portfolio_cost('../Data/portfolio1.dat')