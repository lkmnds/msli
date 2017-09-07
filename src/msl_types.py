import inspect

import msl_error as merror
import msl_env as menv

MSL_VERSION = '0.0.0'
MSL_BUILD = 3

class MslObject:
    def __init__(self, valtype):
        self.type = valtype

    def __repr__(self):
        return "Object(%s)" % repr(self.value)

class MslList(MslObject):
    def __init__(self, lst):
        MslObject.__init__(self, 'list')
        if isinstance(lst, list):
            self.values = lst
            self.hash = tuple(self.values)
        elif isinstance(lst, tuple):
            self.values = list(lst)
            self.hash = lst
        elif isinstance(lst, MslPList):
            self.values = lst.values
        else:
            merror.error("Error creating MslList with %s" % type(lst))

    def _update(self):
        self.hash = tuple(self.values)

    def append(self, v):
        self.values.append(v)
        self._update()

    def extend(self, v):
        self.values.extend(v)
        self._update()

    def __getitem__(self, i):
        return self.values[i]

    def __len__(self):
        return len(self.values)

    def __bool__(self):
        return True

    def __eq__(self, other):
        # compare element by element
        if isinstance(other, MslList) or isinstance(other, MslVector):
            if len(self.values) == len(other.values):
                for i in range(0, len(self.values)):
                    if self.values[i] != other.values[i]:
                        return False
                return True
            else:
                return False
        else:
            return False

    def __hash__(self):
        return hash(self.hash)

    def __repr__(self):
        return "List(%s)" % repr(self.values)

class MslSymbol(MslObject):
    def __init__(self, val=None):
        MslObject.__init__(self, 'symbol')
        self.symval = val

    def __eq__(self, other):
        if isinstance(other, MslSymbol):
            return self.symval == other.symval
        return False

    def __hash__(self):
        return hash(self.symval)

    def __repr__(self):
        return "Symbol(%s)" % repr(self.symval)

class MslNumber(MslObject):
    def __init__(self, num=None):
        MslObject.__init__(self, 'num')

        if isinstance(num, int) or isinstance(num, float):
            self.num = num
        else:
            try:
                self.num = int(num)
            except:
                self.num = float(num)

    # operator functions
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

    def __pow__(self, other):
        return MslNumber(pow(self.num, other.num))

    def __mod__(self, other):
        return MslNumber(self.num % other.num)

    # comparison functions
    def __eq__(self, other):
        if isinstance(other, MslNumber):
            return self.num == other.num
        elif isinstance(other, MslNil) or other == None:
            return False
        else:
            try:
                return self.num == MslNumber(other).num
            except:
                return False

    def __hash__(self):
        return hash(self.num)

    def __lt__(self, other):
        return self.num < other.num

    def __le__(self, other):
        return self.num <= other.num

    def __gt__(self, other):
        return self.num > other.num

    def __ge__(self, other):
        return self.num >= other.num

    def __repr__(self):
        return "Number(%s)" % repr(self.num)

class MslStr(MslObject, str):
    def __new__(cls, *args, **kw):
        return str.__new__(cls, *args, **kw)

    def __init__(self, string):
        MslObject.__init__(self, 'str')
        self.value = string

    def __bool__(self):
        return True

class MslNil(MslObject):
    def __init__(self):
        MslObject.__init__(self, 'nil')
        self.value = None

    def __bool__(self):
        return False

    def __eq__(self, other):
        return other == None

    def __repr__(self):
        return "Nil(%s)" % self.value

class MslBool(MslObject):
    def __init__(self, val=False):
        MslObject.__init__(self, 'bool')
        self.value = val

    def __bool__(self):
        return self.value

    def __and__(self, other):
        return MslBool(self.value and other.value)

    def __or__(self, other):
        return MslBool(self.value or other.value)

    def __repr__(self):
        return "Bool(%s)" % self.value

class MslKeyword(MslObject):
    def __init__(self, val):
        MslObject.__init__(self, 'keyword')

        if val.startswith("\u029e"):
            self.value = val
        else:
            self.value = f'\u029e{val}'

    def __eq__(self, other):
        return self.value == other.value

class MslVector(MslObject):
    def __init__(self, val=[]):
        MslObject.__init__(self, 'vec')
        self.values = val
        self.tup = tuple(self.values)
    def __add__(self, rhs):
        res = MslVector(self.values.__add__(self, rhs))
        self._update()
        return res

    def __getitem__(self, i):
        if type(i) == slice: return MslVector(self.values.__getitem__(self, i))
        elif i >= len(self): return None
        else:                return self.values.__getitem__(i)

    def __getslice__(self, *a):
        return MslVector(self.values.__getslice__(self, *a))

    def _update(self):
        self.tup = tuple(self.values)

    def append(self, v):
        self.values.append(v)
        self._update()

    def __len__(self):
        return len(self.values)

    def __bool__(self):
        return True

    # comparison functions
    def __eq__(self, other):
        # compare element by element
        if isinstance(other, MslList) or isinstance(other, MslVector):
            if len(self.values) == len(other.values):
                for i in range(0, len(self.values)):
                    if self.values[i] != other.values[i]:
                        return False
                return True
            else:
                return False
        else:
            return False

    def __hash__(self):
        return hash(self.tup)

    def __repr__(self):
        return "Vector(%s)" % self.values

class MslPList(MslObject):
    def __init__(self, val=[]):
        MslObject.__init__(self, 'plist')
        self.values = val

    def __getitem__(self, i):
        return self.values[i]

    def __repr__(self):
        return "P_List(%s)" % self.values

class MslCList(MslList):
    def __init__(self, val=[]):
        MslList.__init__(self, val)
        self.type = 'clist'

class MslHashmap(MslObject):
    def __init__(self, val=[]):
        MslObject.__init__(self, 'hashmap')
        self.hm = {}
        for i in range(0, len(val), 2):
            self.hm[val[i]] = val[i+1]
        self.values = self.hm

    def append(self, value):
        print(value)

    def __repr__(self):
        return "Hashmap(%s)" % self.hm

class MslFunction(MslObject):
    def __init__(self, evalfunc, envclass, ast, env, params):
        MslObject.__init__(self, 'function')

        def fn(*args):
            return evalfunc(ast, envclass(env, params, MslList(args)))

        fn.__meta__ = None
        fn.__ast__ = ast
        fn.__gen_env__ = lambda args: envclass(env, params, args)

        self.func = fn
        self.args = params

    def __call__(self, *args):
        return self.func(*args)

    def __repr__(self):
        return "Function(%s)" % repr(self.args)

class MslAtom(MslObject):
    def __init__(self, v):
        MslObject.__init__(self, 'atom')
        self.value = v

    def __repr__(self):
        return "Atom(%s)" % repr(self.value)

def py_to_msl(obj):
    if isinstance(obj, bool):
        return MslBool(obj)
    elif isinstance(obj, int) or isinstance(obj, float):
        return MslNumber(obj)
    elif isinstance(obj, str):
        return MslStr(obj)
    elif isinstance(obj, list) or isinstance(obj, list):
        return MslList(obj)
    elif isinstance(obj, dict):
        feeder = []
        for k in obj:
            feeder.append(k)
            feeder.append(obj[k])
        return MslHashmap(feeder)
    elif callable(obj):
        params = []
        sig = inspect.signature(obj)
        for param in sig.parameters:
            param_obj = sig.parameters[param]
            params.append(param_obj.name)

        return MslFunction(obj, menv.Enviroment, None, None, params)
    else:
        merror.error("pytomsl: no instance found of %s" % type(obj))
        return None
