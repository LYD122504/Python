from ..formatter import TableFormatter
class HTMLTableFormatter(TableFormatter):
    def headings(self,headers):
        print('<tr>',end=' ')
        for h in headers:
            print('<th>%s</th>' % h,end=' ')
        print('</tr>')
    def row(self,rowdata):
        print('<tr>',end=' ')
        for r in rowdata:
            print('<td>%s</td>' % r,end=' ')
        print('</tr>')