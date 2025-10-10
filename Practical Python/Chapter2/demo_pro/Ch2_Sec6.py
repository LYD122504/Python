# Creating new lists
a=[1,2,3,4,5]
b=[2*x for x in a ]
print(b)

names=['Liyaoda','Bob','Alice']
a=[name.lower() for name in names]
print(a)

a=(1,2,3,4,5)
b=[2*x for x in a ]
print(b)

# Filtering lists
a=[1,-5,4,2,-2,10]
b=[2*x for x in a if x>0]
print(b)