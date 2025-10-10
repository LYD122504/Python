name='IBM'
shares=100
price=91.1
# ^表示居中展示
print(f"{name:^10s} {shares:>10d} {price:>10.2f}")

# 利用format_map()方法可以把字符格式化映射到字典上
s={
    'name':'IBM',
    'shares':100,
    'price':91.1
}
st='{name:^10s} {shares:>10d} {price:>10.2f}'
print(st.format_map(s))

# format方法
print(st.format(name='IBM',shares=100,price=91.1))
st='{:<10s} {:<10d} {:<10.2f}'
print(st.format('IBM',100,91.1))

# % 格式字符
print('The value is %d' % 3)
print('%5d %-5d %10d'%(3,4,5))
print('%0.2f' %3.1415926)
# 字节字符串的作用
print(b'%s has %d messages' % (b'Dave', 37))
print(b'%b has %d messages' % (b'Dave', 37))

bstr=b'Dave'
bstr=bstr.decode('utf-8')
print(f"{bstr:^10s} {shares:>10d} {price:>10.2f}")
