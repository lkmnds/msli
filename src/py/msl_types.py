
class MslObject:
    def __init__(self, valtype):
        self.type = valtype

    def __repr__(self):
        return repr(self.value)

class MslList(MslObject):
    def __init__(self, lst):
        MslObject.__init__(self, 'list')
        self.values = lst

    def append(self, v):
        self.values.append(v)

    def __len__(self):
        return len(self.values)

    def __repr__(self):
        return repr(self.values)

class MslSymbol(MslObject):
    def __init__(self, val=None):
        MslObject.__init__(self, 'symbol')
        self.symval = val
    def __repr__(self):
        return repr(self.symval)

class MslNumber(MslObject):
    def __init__(self, num=None):
        MslObject.__init__(self, 'num')
        self.num = int(num)

    def __add__(self, other):
        return MslNumber(self.num + other.num)

    def __sub__(self, other):
        return MslNumber(self.num - other.num)

    def __mul__(self, other):
        return MslNumber(self.num * other.num)

    def __div__(self, other):
        return MslNumber(self.num / other.num)

    def __truediv__(self, other):
        return MslNumber(self.num / other.num)

    def __repr__(self):
        return repr(self.num)

class MslStr(MslObject, str):
    def __new__(cls, *args, **kw):
        return str.__new__(cls, *args, **kw)
    def __init__(self, string):
        MslObject.__init__(self, 'str')
        self.value = string

class MslNil(MslObject):
    def __init__(self):
        MslObject.__init__(self, 'nil')

class MslBool(MslObject):
    def __init__(self, val=False):
        MslObject.__init__(self, 'bool')
        self.value = val

class MslKeyword(MslObject):
    def __init__(self, val):
        MslObject.__init__(self, 'keyword')
        if val[0] == "\u029e":
            self.value = val
        else:
            self.value = "\u029e" + val

class MslVector(MslObject):
    def __init__(self, val=[]):
        MslObject.__init__(self, 'vec')
        self.values = val
    def __add__(self, rhs): return MslVector(self.values.__add__(self, rhs))
    def __getitem__(self, i):
        if type(i) == slice: return MslVector(self.values.__getitem__(self, i))
        elif i >= len(self): return None
        else:                return self.value.__getitem__(self, i)
    def __getslice__(self, *a): return MslVector(self.values.__getslice__(self, *a))

    def append(self, v):
        self.values.append(v)

    def __len__(self):
        return len(self.values)

class MslHashmap(MslObject):
    def __init__(self, val=[]):
        MslObject.__init__(self, 'hashmap')
        self.hm = {}
        for i in range(0, len(val), 2):
            self.hm[val[i]] = val[i+1]
        self.values = self.hm
    def append(self, value):
        print(value)
