import inspect
import sys
class Structure():
    @classmethod
    def create_init(cls):
        argstr=','.join(cls._fields)
        code = f'def __init__(self, {argstr}):\n'
        for name in cls._fields:
            code+=f'    self.{name}={name}\n'
        locs={ }
        exec(code,locs)
        cls.__init__=locs['__init__']
    @classmethod
    def set_fields(cls):
        sig=inspect.signature(cls.__init__)
        cls._fields=tuple(sig.parameters)
    @staticmethod
    def _init():
        locs=sys._getframe(1).f_locals # Get callers local variables
        self = locs['self']
        for name, val in locs.items():
            if name == 'self': continue
            setattr(self, name, val)
    def __repr__(self):
        result=''
        for i in range(len(self._fields)):
            result+=str(getattr(self,self._fields[i]))
            if i!=len(self._fields)-1:
                result+=','
        return f'{self.__class__.__name__}({result})'
    def __setattr__(self, name, value):
        if name[0]!='_' and name not in self._fields:
            raise AttributeError('No attribute %s' % name)
        self.__dict__[name]=value