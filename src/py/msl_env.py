
import msl_types as mtypes
import msl_error as merror

class Enviroment:
    def __init__(self, outer={}, binds=[], exprs=[]):
        self.data = {}
        self.outer = outer or None

        if binds:
            for i in range(0, len(binds)):
                print('binds', binds[i])
                if binds[i].symval == '&':
                    print('b', binds[i+1].symval, exprs[i:])
                    self.data[binds[i+1].symval] = exprs[i:]
                    break
                else:
                    self.data[binds[i].symval] = exprs[i]

    def set(self, k, v):
        if isinstance(k, mtypes.MslSymbol):
            print("warning: setting symbol %s as key" % k.symval)
            k = k.symval
        self.data[k] = v
        return v

    def find(self, symbol):
        if isinstance(symbol, mtypes.MslSymbol):
            print("warning: finding a symbol %s" % symbol.symval)
            symbol = symbol.symval

        # print("env: find %s (%s)" % (symbol, type(symbol)))

        if symbol in self.data:
            return self
        elif self.outer:
            return self.outer.find(symbol)
        else:
            merror.debug("env.debug: no env found for %s" % symbol)
            return None

    def get(self, symbol):
        if isinstance(symbol, mtypes.MslSymbol):
            print("warning: getting a symbol %s" % symbol.symval)
            symbol = symbol.symval

        env = self.find(symbol)
        if not env:
            raise Exception("enviroment: Symbol %s not found" % symbol)
        return env.data[symbol]
