# typedproperty.py

class TypedProperty:
    """
    类型检查的描述符，使用 __set_name__ 自动捕获属性名
    """
    def __init__(self, expected_type):
        self.expected_type = expected_type
        self.private_name = None  # 将由 __set_name__ 设置
    
    def __set_name__(self, owner, name):
        """当描述符被放置在类中时自动调用"""
        self.private_name = '_' + name
    
    def __get__(self, instance, cls):
        if instance is None:
            return self
        return getattr(instance, self.private_name)
    
    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(f'Expected {self.expected_type.__name__}')
        setattr(instance, self.private_name, value)


# 工厂函数：创建特定类型的描述符
def String():
    return TypedProperty(str)

def Integer():
    return TypedProperty(int)

def Float():
    return TypedProperty(float)