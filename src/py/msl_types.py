
class MslType:
    def __init__(self, valtype):
        self.type = valtype

class MslList(MslType):
    def __init__(self, lst):
        MslType.__init__(self, 'list')
        self.values = lst

class MslSymbol(MslType):
    def __init__(self, val=None):
        MslType.__init__(self, 'symbol')
        self.symval = val

class MslNumber(MslType):
    def __init__(self, num=None):
        MslType.__init__(self, 'num')
        self.num = int(num)

class MslStr(MslType, str):
    def __new__(cls, *args, **kw):
        return str.__new__(cls, *args, **kw)
    def __init__(self, string):
        MslType.__init__(self, 'str')
        self.value = string

class MslNil(MslType):
    def __init__(self):
        MslType.__init__(self, 'nil')

class MslBool(MslType):
    def __init__(self, val=False):
        MslType.__init__(self, 'bool')
        self.value = val
