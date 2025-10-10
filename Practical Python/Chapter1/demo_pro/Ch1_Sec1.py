# 1.1 Introduction to Python

print('Hello, World!')

a=3+4
b=a*2
print(b)

height=442
print(type(height))
height=442.0
print(type(height))
height='Really tall'
print(type(height))

if a>b:
    print('a is greater than b')
else:
    print('b is greater than or equal to a')

if a > b:
    print('Computer says no')
elif a == b:
    print('Computer says yes')
else:
    print('Computer says maybe')

name = input('Enter your name\n:')
print('Your name is', name)

age = input('Enter your age\n:')
age=int(age)
age=age+1
print('Your age is', age)

num_list=list(map(int,input('Enter some integers:').split()))
print(num_list)

if a>b:
	pass
else:
	print("a is less than or equal to b")