import sys
import fileparse
import report

if len(sys.argv) != 3:
    raise SystemExit(f'Usage: {sys.argv[0]} ' 'portfile pricefile')
portfile = sys.argv[1]
pricefile = sys.argv[2]

report.portfolio_report(portfile,pricefile)

import os

print(os.environ['NAME']) # 'dave'