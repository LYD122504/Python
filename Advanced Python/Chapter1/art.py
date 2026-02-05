import sys
import random
chars='\|/'
def draw(rows,columns):
    for r in range(rows):
        print(''.join(random.choice(chars) for _ in range(columns))
)
if __name__=='__main__':
    if len(sys.argv)!=3:
        raise SystemExit(f'Usage: {sys.argv[0]} rows columns')
    draw(int(sys.argv[1]),int(sys.argv[2]))