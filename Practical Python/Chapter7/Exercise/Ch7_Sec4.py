from timethis import timethis
@timethis
def countdown(n):
    while n>0:
        n-=1
a=countdown(1000000)
print(a)
