
import msl_types as mtypes
import msl_error as merror

class Enviroment:
    def __init__(self, outer={}, binds=[], exprs=[]):
        self.data = {}
        self.outer = outer or None

        if binds:
            for i in range(0, len(binds)):
                if binds[i].symval == '&':
                    self.data[binds[i+1].symval] = exprs[i:]
                    break
                else:
                    self.data[binds[i].symval] = exprs[i]

    def set(self, k, v):
        if isinstance(k, mtypes.MslSymbol):
            merror.debug(f'warning: setting symbol {k.symval!r} as key')
            k = k.symval
        self.data[k] = v
        return v

    def find(self, symbol):
        if isinstance(symbol, mtypes.MslSymbol):
            merror.debug(f'warning: finding sym {symbol.symval!r}')
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
            merror.debug(f'warning: getting a symbol {sumbol.symval!r}')
            symbol = symbol.symval

        env = self.find(symbol)
        if not env:
            raise RuntimeError(f'environment: Symbol {symbol!r} not found')

        return env.data[symbol]
