import fileparse

with open("./data/portfolio.csv") as f:
    first_line = f.readline()
    print("Raw first line:", repr(first_line))
    print("Split by tabs :", first_line.split("\t"))
    print("Split by space:", first_line.split())

