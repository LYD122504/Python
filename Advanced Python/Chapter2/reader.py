import csv
def read_csv_as_dicts(filename,types):
    records=[]
    with open(filename) as f:
        rows=csv.reader(f)
        headers=next(rows)
        for row in rows:
            record={name:func(val) for name,func,val in zip(headers,types,row)}
            records.append(record)
        return records