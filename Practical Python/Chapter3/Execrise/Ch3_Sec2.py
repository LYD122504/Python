# Ex3.3
import csv

def parse_csv(filename,has_header=True,select=[],type=[],delimiter=','):
    '''
    Parse a csv into a list of records
    '''
    with open(filename) as f:
        rows = csv.reader(f,delimiter=delimiter)
        # Read the file headers
        if has_header:
            headers = next(rows)
            if select:
                h_index=[headers.index(item) for item in select]
                headers=[headers[item] for item in h_index]
            else:
                h_index=list(range(len(headers)))
        records=[]
        for row in rows:
            if not row: # Skip rows with no data
                continue
            if has_header:
                row=[row[item] for item in h_index]
                if type:
                    row=[func(item) for func,item in zip(type,row)]
                record=dict(zip(headers,row))
            else:
                record=tuple(row)
            records.append(record)
    return records

portfolio=parse_csv('portfolio.csv',has_header=True,select=[],type=[],delimiter=',')
print(portfolio)