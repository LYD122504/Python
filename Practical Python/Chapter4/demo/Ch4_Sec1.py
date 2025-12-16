# Instance for OOP
nums=[1,2,3]
print(nums)
nums.append(4)
print(nums)
nums.insert(1,10)
print(nums)

# class实例
class Player:
    counter=0
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.health=100
        Player.counter+=1
    def move(self,dx,dy):
        self.x+=dx
        self.y+=dy
    def left(self,amt):
        self.move(-amt,0)
    def damage(self,pts):
        self.health-=pts

a=Player(2,3)
print(a.counter)
print(a.__dict__)
b=Player(3,4)
print(b.counter)
print(b.__dict__)

# Python 私有成员
class BB():
    def __init__(self,name):
        self.__name=name
    def get_name(self):
        return self.__name

b=BB('bb')
d=BB('dd')
b.__name='cc'
print(b.__name)
print(b.get_name())
print(d.get_name())
print(d.__name)
