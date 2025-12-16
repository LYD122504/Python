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
        raise RuntimeError(f'Unknown format {fmt}')