from follow import follow
import csv
import report
import tableformatter

def select_columns(rows, indices):
    return ([row[index] for index in indices] for row in rows)
def parse_stock_data(lines):
    rows = csv.reader(lines)
    rows = select_columns(rows, [0, 1, 4])
    rows = convert_types(rows, [str, float, float])
    rows = make_dicts(rows, ['name', 'price', 'change'])
    return rows

def convert_types(rows, types):
    return ([func(val) for func, val in zip(types, row)] for row in rows)

def make_dicts(rows, headers):
    return (dict(zip(headers, row)) for row in rows)

def filter_symbols(rows, names):
    return (row for row in rows if row['name'] in names)
def ticker(filename1,filename2,fmt):
    portfolio=report.read_portfolio(filename1)
    lines=follow(filename2)
    rows=parse_stock_data(lines)
    rows = (row for row in rows if row['name'] in portfolio)
    formatter = tableformatter.create_fun(fmt)
    formatter.headings(['Name','Price','Change'])
    for row in rows:
        formatter.row([ row['name'], f"{row['price']:0.2f}", f"{row['change']:0.2f}"] )

if __name__=='__main__':
    ticker('../data/portfolio.csv','stocklog.csv','txt')