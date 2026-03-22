import csv
from abc import ABC,abstractmethod
class CSVParser(ABC):
    def parse(self,filename):
        records=[]
        with open(filename) as f:
            rows=csv.reader(f)
            self.headers=next(rows)
            for row in rows:
                record=self.make_record(self.headers,row)
                records.append(record)
            return records
    @abstractmethod
    def make_record(self,headers,row):
        raise RuntimeError('Must Implemented')
class DictCSVParser(CSVParser):
    def __init__(self, types):
        self.types = types
    def make_record(self, headers, row):
        return { name: func(val) for name, func, val in zip(headers, self.types, row) }
class InstanceCSVParser(CSVParser):
    def __init__(self, cls):
        self.cls = cls
    def make_record(self, headers, row):
        return self.cls.from_row(row)
def read_csv_as_dicts(filename,types):
    read_dict=DictCSVParser(types)
    return read_dict.parse(filename)
def read_csv_as_instances(filename,cls):
    read_cls=InstanceCSVParser(cls)
    return read_cls.parse(filename)
__all__=['read_csv_as_dicts','read_csv_as_instances']