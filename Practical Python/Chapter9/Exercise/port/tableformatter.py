class TableFormatter:
    def headings(self,headers):
        '''
        Emit the table headings.
        '''
        raise NotImplementedError()
    def row(self,rowdata):
        '''
        Emit a single row of table data.
        '''
        raise NotImplementedError()

class FormatError(Exception):
    pass

class Textformatter(TableFormatter):
    '''
    Emit a table in plain-text format
    '''
    def headings(self,headers):
        for h in headers:
            print(f'{h:>10s}', end=' ')
        print()
        print(('-'*10 + ' ')*len(headers))

    def row(self,rowdata):
        for d in rowdata:
            print(f'{d:>10s}',end=' ')
        print()
class CSVformatter(TableFormatter):
    def headings(self,headers):
        s=','
        s=s.join(headers)
        print(s)
    def row(self,rowdata):
        s=','
        s=s.join(rowdata)
        print(s)
class HTMLformatter(TableFormatter):
    def headings(self,headers):
        s='</th><th>'
        s='<tr><th>'+s.join(headers)+'</th></tr>'
        print(s)
    def row(self,rowdata):
        s='</td><td>'
        s='<tr><td>'+s.join(rowdata)+'</td></tr>'
        print(s)

def create_fun(fmt):
    if fmt=='txt':
        return Textformatter()
    elif fmt=='csv':
        return CSVformatter()
    elif fmt=='html':
        return HTMLformatter()
    else:
        raise FormatError(f'Unknown table format {fmt}')

def print_table(objects, columns, formatter):
    '''
    Make a nicely formatted table from a list of objects and attribute names.
    '''
    formatter.headings(columns)
    for obj in objects:
        rowdata = [ str(getattr(obj, name)) for name in columns ]
        formatter.row(rowdata)