def logged_getattr(cls):
    # Get the original implementation
    orig_getattribute=cls.__getattribute__
    # Replacement method
    def __getattribute__(self,name):
        print("Getting:",name)
        return orig_getattribute(self,name)
    # Attach to the class
    cls.__getattribute__=__getattribute__
    return cls
@logged_getattr
class MyClass:
    def __init__(self,name,size):
        self.name=name
        self.size=size
    def foo(self):
        pass
s=MyClass(10,9)
print(s.name)
print(s.size)
s.foo()

class PluginBase:
    subclasses = []

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # 只要有人继承我，我就把它存到列表里，实现自动注册
        cls.subclasses.append(cls)

class VideoPlugin(PluginBase): pass
class AudioPlugin(PluginBase): pass

print(PluginBase.subclasses) 
# 输出: [<class 'VideoPlugin'>, <class 'AudioPlugin'>]