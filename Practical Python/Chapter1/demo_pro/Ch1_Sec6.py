f=open('./fun.txt','r+')
f.write('Hello world!\nThis is a test file.\n')
f.seek(0)
data=f.read(2)
print(data)
data=f.read()
print(data)
f.close()

with open('foo.txt', 'rt') as file:
    for line in file:
        print(line.strip())