# Ex3.3
import csv

def parse_csv(filename,has_header=True,select=[],type=[],delimiter=',',silence_error=False):
    '''
    Parse a csv into a list of records
    '''
    with open(filename) as f:
        rows = csv.reader(f,delimiter=delimiter)
        # Read the file headers
        if has_header==False and len(select)>0:
            raise RuntimeError("select argument requires column headers")
        if has_header:
            headers = next(rows)
            if select:
                h_index=[headers.index(item) for item in select]
                headers=[headers[item] for item in h_index]
            else:
                h_index=list(range(len(headers)))
        records=[]
        row_number=0
        for row in rows:
            row_number+=1
            if not row: # Skip rows with no data
                continue
            if select:
                row=[row[item] for item in h_index]
            if type:
                try:
                    row=[func(item) for func,item in zip(type,row)]
                except Exception as e:
                    if not silence_error:
                        print(f"Row {row_number}: Couldn't convert {row}")
                        print(f"Row {row_number}: Reason {e}")
                        continue 
            if has_header:   
                record=dict(zip(headers,row))
            else:
                record=tuple(row)
            records.append(record)
    return records

portfolio=parse_csv('./data/missing.csv',has_header=True,select=[],type=[str, int, float],delimiter=',',silence_error=True)
print(portfolio)