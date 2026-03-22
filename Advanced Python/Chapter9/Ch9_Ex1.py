from follow import follow
import sys
print(globals())
print(list(sys.modules))
from bar import *
grok(2)
foo(3)
print(sys.path)
# Module Loading and System Path
import simplemod
simplemod.foo()
# Repeated Module Loading
simplemod.x=13
import simplemod
import importlib
importlib.reload(simplemod)
print(simplemod.x)
print(sys.modules['simplemod'])
del sys.modules['simplemod']
# From module import
from simplemod import x,foo
x=12
foo()