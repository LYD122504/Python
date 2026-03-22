from structly.tableformat.formats.text import TextTableFormatter
print(TextTableFormatter.__module__)
print(TextTableFormatter.__module__.split('.')[-1])
from structly.tableformat.formatter import TableFormatter
print(TableFormatter._formats)