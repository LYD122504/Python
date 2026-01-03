# Exercise 6.13 Generator Expression
nums=[1,2,3,4,5]
squares=(x*x for x in nums)
print(squares)
for n in squares:
    print(n)
for n in squares:
    print(n)  # No output, as the generator is exhausted

# Exercise 6.14 Generator Expression in Function Arguments
nums=[1,2,3,4,5]
print(sum([x*x for x in nums]))  # Using list comprehension
print(sum(x*x for x in nums))    # Using generator expression