from pprint import pprint
portfolio=[
    ('GOOG', 100, 490.1),
    ('IBM', 50, 91.1),
    ('CAT', 150, 83.44),
    ('IBM', 100, 45.23),
    ('GOOG', 75, 572.45),
    ('AA', 50, 23.15)
]
pprint(portfolio)

# Counter计数器
from collections import Counter
# 实例化空对象
d=Counter()
print(d)
# 利用可迭代对象实例化
d=Counter(portfolio)
pprint(d)
# 利用字典实例化
d=Counter({'a':1, 'b':2, 'c':5})
pprint(d)
# 利用关键字参数实例化
d1=Counter(a=1, b=1, c=3,d=4)
pprint(d1)
# 运算
print(d+d1)
print(d1-d)
print(d&d1)
print(d|d1)

# 合并股份
d=Counter()
for name,share,price in portfolio:
    d[name]+=share
pprint(d)

# 一对多映射
from collections import defaultdict
d1=dict()
d=defaultdict(int)
print(d['a'])
# print(d1['a']) 报错keyError

holdings=defaultdict(list)
for name,share,price in portfolio:
    holdings[name].append((share,price))
pprint(holdings)

# deque 双端队列
from collections import deque
d=deque([1,2,3])
print(d)
d.append(4) # 右侧添加
print(d)
d.appendleft(0) # 左侧添加
print(d)
print(d.pop()) # 右侧弹出
print(d)
print(d.popleft())  # 左侧弹出
print(d)
d.extend([4,5,6]) # 右侧添加多个
print(d)
d.extendleft([-1,-2,-3]) # 左侧添加多个，顺序相反
print(d)
print(d[0]) # 访问元素
print(d[-1])
d.rotate(1) # 向右旋转
print(d)
d=deque(maxlen=3) # 限定最大长度
d.extend([1,2,3,4,5])
print(d)