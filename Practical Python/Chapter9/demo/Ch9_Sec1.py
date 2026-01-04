import pack.report
port=pack.report.read_portfolio('../data/portfolio.csv')
print(port)
import sys
pack.report.main(sys.argv[1:])