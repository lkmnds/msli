
import msl_printer as printer

import msl_types as mtypes

def make_list(*args):
    return mtypes.MslList(args)

def prn(x):
    print(printer.pr_str(x, True))
    return

ns = {
    '+': lambda x,y: x+y,
    '-': lambda x,y: x-y,
    '/': lambda x,y: x/y,
    '*': lambda x,y: x*y,

    'prn': prn,
    'list': make_list,
    'list?': lambda x: isinstance(x, mtypes.MslList),
    'empty?': lambda x: len(x) == 0,
    'count': lambda x: len(x),

    '=':  lambda x,y: x == y,
    '<':  lambda x,y: x <  y,
    '<=': lambda x,y: x <= y,
    '>':  lambda x,y: x  > y,
    '>=': lambda x,y: x >= y,
}
