from abc import ABC,abstractmethod
import csv
class IStream(ABC):
    @abstractmethod
    def read(self,maxtypes=None):
        pass
    @abstractmethod
    def write(self,data):
        pass
class CSVParser:
    def parse(self,filename):
        records=[]
        with open(filename) as f:
            rows=csv.reader(f)
            self.headers=next(rows)
            for row in rows:
                record=self.make_record(row)
                records.append(record)
            return records
    def make_record(self,row):
        raise RuntimeError('Must Implemented')
class DictCSVParser(CSVParser):
    def make_record(self, row):
        return dict(zip(self.headers, row))
parser = DictCSVParser()
portfolio = parser.parse('../Data/portfolio.csv')    
import stock, reader, tableformat
portfolio = reader.read_csv_as_instances('../Data/portfolio.csv', stock.Stock)
class NewFormatter(tableformat.TableFormatter):
    def headers(self, headings):
        pass
    def row(self, rowdata):
        pass
f = NewFormatter()