import inspect
class Validator:
    def __init__(self,name=None):
        self.name=name
    @classmethod
    def check(cls,value):
        return value
    def __set_name__(self,cls,name):
        self.name=name
    def __set__(self,instance,value):
        instance.__dict__[self.name]=self.check(value)
class Typed(Validator):
    expected_type=object
    @classmethod
    def check(cls,value):
        if not isinstance(value,cls.expected_type):
            raise TypeError(f'Expected{cls.expected_type}')
        return super().check(value)
class Integer(Typed):
    expected_type=int
class Float(Typed):
    expected_type=float
class String(Typed):
    expected_type=str
class Positive(Validator):
    @classmethod
    def check(cls,value):
        if value<0:
            raise ValueError('Expected >=0')
        return super().check(value)
class NotEmpty(Validator):
    @classmethod
    def check(cls,value):
        if len(value)==0:
            raise ValueError('Must be non-empty')
        return super().check(value)
class PositiveInteger(Integer,Positive):
    pass
class PositiveFloat(Float,Positive):
    pass
class NonEmptyString(String,NotEmpty):
    pass
class ValidatedFunction:
    def __init__(self,func):
        self.func=func
    def __call__(self,*args,**kwargs):
        sig=inspect.signature(self.func)
        bound=sig.bind(*args,**kwargs)
        annotations=self.func.__annotations__
        for name,val in bound.arguments.items():
            if name in annotations:
               expected_test=annotations[name]
            expected_test.check(val) 
        print('Calling',self.func)
        result=self.func(*args,**kwargs)
        return result
    def __get__(self, instance, owner):
        if instance is None:
            return self
        # 返回一个绑定了 instance 的新可调用对象
        from functools import partial
        return partial(self, instance)