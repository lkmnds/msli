
import msl_types as mtypes

class Enviroment:
    def __init__(self, outer={}):
        self.data = {}
        self.outer = outer or None

    def set(self, k, v):
        self.data[k] = v
        print("set %s to %s" % (k,v))
        return v

    def find(self, symbol):
        if isinstance(symbol, mtypes.MslSymbol):
            print("warning: finding a symbol")
            symbol = symbol.symval
        print("env: find %s (%s)" % (symbol, type(symbol)))
        if symbol in self.data:
            return self
        elif self.outer:
            return self.outer.find(symbol)
        else:
            print("env.debug: no env found for %s" % symbol)
            return None

    def get(self, symbol):
        if isinstance(symbol, mtypes.MslSymbol):
            print("warning: getting a symbol")
            symbol = symbol.symval

        env = self.find(symbol)
        if not env:
            raise Exception("enviroment: Symbol %s not found" % symbol)
        return env.data[symbol]
