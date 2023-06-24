class Singleton(object):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = object.__new__(cls, *args, **kwargs)
            cls._instance.initialize(*args, **kwargs)
        return cls._instance

    def initialize(self, *args, **kwargs):
        # 公用内容可以放到这里进行初始化，这样就不会重复执行
        self.a = 123

    def __init__(self):
        # 每个实例函数仍然会执行构造函数
        print("__init__")
