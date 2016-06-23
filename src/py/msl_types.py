
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
