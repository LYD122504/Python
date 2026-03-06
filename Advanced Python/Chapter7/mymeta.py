class mytype(type):
    @staticmethod
    def __new__(meta,name,bases,methods):
        print('Creating class:',name)
        print('Base classes:',bases)
        print('Methods:',list(methods))
        return super().__new__(meta,name,bases,methods)
    
class myobject(metaclass=mytype):
    pass