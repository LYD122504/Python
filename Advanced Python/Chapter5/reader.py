# 撤销掉类的定义
import csv
import logging
log=logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
from typing import List,Dict,Callable,Iterable
def convert_csv(lines,func,*,headers=None):
    records=[]
    rows=csv.reader(lines)
    if headers is None:
        headers=next(rows)
    for row in rows:
        record=func(row,headers)
        records.append(record)
    return records
    
def csv_as_dicts(lines:Iterable,types:List[Callable],*,headers:List[str]=None)->List[Dict]:
    '''
    Read CSV data into a list of dictionaries with optional type conversion
    '''
    records=[]
    rows=csv.reader(lines)
    if headers is None:
        headers=next(rows)
    for it,row in enumerate(rows):
        try:
            record={name:func(val) for name,func,val in zip(headers,types,row)}
            records.append(record)
        except ValueError:
            log.warning('Row %s: Bad row: %s', it+1, row)
            log.debug('Row %s: Reason: %s', it+1, row)
    return records
def csv_as_instances(lines:Iterable,cls,*,headers=None):
    '''
    Read CSV data into a list of instances
    '''
    records=[]
    rows=csv.reader(lines)
    if headers is None:
        headers=next(rows)
    for row in rows:
        record=cls.from_row(row)
        records.append(record)
    return records
def read_csv_as_dicts(filename,types,*,headers=None):
    '''
    Read CSV data into a list of dictionaries with optional type conversion
    '''
    with open(filename) as file:
        return csv_as_dicts(file,types,headers=headers)
def read_csv_as_instances(filename,cls,*,headers=None):
    '''
    Read CSV data into a list of instances
    '''
    with open(filename) as file:
       return csv_as_instances(file,cls,headers=headers)