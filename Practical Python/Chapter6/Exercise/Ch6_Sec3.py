# Exercise 6.8: Setting up a simple pipeline
def filematch(lines, substr):
        for line in lines:
            if substr in line:
                yield line
if __name__=='__main__':
    from follow import follow
    import csv
    lines=follow('stocklog.csv')
    '''
    ibm=filematch(lines,'"IBM"')
    for line in ibm:
         print(line)'''
    
#Exercise 6.9: Setting up a more complex pipeline
    rows=csv.reader(lines)
    for row in rows:
         print(row)