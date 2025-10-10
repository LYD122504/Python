# Extracting individual characters and substrings
symbols='AAPL,IBM,MSFT,YHOO,SCO'
print(symbols)
print(symbols.lower())
print(symbols[0])
print(symbols[0:4])
print(symbols[-3:])

# String concatenation
symbols=symbols+'GOOG'
print(symbols)
symbols=symbols[0:-4]
print(symbols)
symbols=symbols+',GOOG'
print(symbols)
symbols='HPQ,'+symbols
print(symbols)

# Membership testing (substring testing)
print('IBM' in symbols)
print('AA' in symbols)
print('CAT' in symbols)

# String Methods
print(symbols.find('IBM'))
print(symbols.find('CAT'))

print(symbols.replace('SCO','DOA'))
print(symbols)
symbols=symbols.replace('SCO','DOA')
print(symbols)

name='   IBM   \n'
print(name.strip())

# f-strings
name='IBM'
shares=100
prices=91.1
print(f'{shares} shares of {name} at ${prices:0.2f}')