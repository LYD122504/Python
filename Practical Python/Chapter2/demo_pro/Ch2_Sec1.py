email_address=None
if email_address:
    print("You have an email address.")
else :
    print("You don't have an email address.")

sv='GOOG',100,490.1
print(sv)
s=()
print(s)
s='a'
print(s)
s=('GOOG',100,490.1)
print(s)

name=s[0]
shares=s[1]
price=s[2]

print(name,shares,price)

snew=(s[0],100,s[2]*1.25)
print(snew)

name,shares,price=s
print(name,shares,price)

s={
    'name':'GOOG',
    'shares':100,
    'price':490.1
}
print(s)
print(f'name: {s["name"]}\nshares: {s["shares"]}\nprice: {s["price"]}')

s['shares']+=100
print(s)
s['date']='6/6/2024'
print(s)

del s['date']
print(s)