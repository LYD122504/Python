import readrides
from collections import Counter
from collections import defaultdict
from collections import deque
rows=readrides.dict_readv2()
# Bus routes number
set_routes={r['route'] for r in rows}
list_routes=list(set_routes)
print(f'Number of bus routes: {len(set_routes)}')
def number_of_rides(route,date):
    for r in rows:
        if r['route']==route and r['date']==date:
            return r['rides']
    return 0
print('Rides on route 22 on 02/02/2011:',number_of_rides('22','02/02/2011'))
print('Rides on route 22 on 02/01/2011:',number_of_rides('22','02/01/2026'))
routine_rides=Counter()
for r in rows:
    routine_rides[r['route']]+=r['rides']
print(routine_rides.most_common(3))
dict_year_routes=defaultdict(Counter)
for r in rows:
    year=r['date'].split('/')[2]
    dict_year_routes[year][r['route']]+=r['rides']
differ=dict_year_routes['2011']-dict_year_routes['2001']
print(differ.most_common(5))

c1 = Counter(a=5, b=3, c=2)
c2 = Counter(a=2, b=4, d=1)
result = c1 - c2
print(result)  # Output: Counter({'a': 3, 'c': 2})

history=deque(maxlen=3)
with open('../Data/ctabus.csv','r') as f:
    for line in f:
        history.append(line.strip())
print('Last 3 lines in the file:')
for record in history:
    print(record)

from collections import ChainMap
defaults={'color':'red','user':'guest'}
env_vars={'user':'alice'}
cli_args={'color':'blue'}
config=ChainMap(cli_args,env_vars,defaults)
print('Color:',config['color'])
print('User:',config['user'])
config['debug'] = True
print(cli_args)

print(config.maps)
a=config.maps
a.append({'debugs': False})
print(config.maps)
print('Debug:',config['debugs'])
new_config=config.new_child({'temp': 42})
print(new_config.maps)
print('Other',new_config.parents)

d1 = {'a': 1, 'b': 2}
d2 = {'b': 3, 'c': 4}

merged = d1 | d2
print(merged)  # {'a': 1, 'b': 3, 'c': 4}
a,*rest,b=[1,2,3,4,5]
print(a,rest,b)

a=(1,2)
b=(3,4)
c=a+b
print(c)

a=[1,2]
b=[3,4]
c=a+b
print(c)