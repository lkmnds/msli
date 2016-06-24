
import msl_printer as printer

import msl_types as mtypes

import operator

def make_list(*args):
    return mtypes.MslList(args)

def prn(x):
    print(printer.pr_str(x, True))
    return

def general_op(x, y, op):
    # treat x and y as mtypes
    if not hasattr(x, 'type'):
        x = mtypes.py_to_msl(x)

    if not hasattr(y, 'type'):
        y = mtypes.py_to_msl(y)

    return op(x, y)

ns = {
    '+': lambda x,y: general_op(x, y, operator.add),
    '-': lambda x,y: general_op(x, y, operator.sub),
    '/': lambda x,y: general_op(x, y, operator.truediv),
    '*': lambda x,y: general_op(x, y, operator.mul),

    'prn': prn,
    'list': make_list,
    'list?': lambda x: isinstance(x, mtypes.MslList),
    'empty?': lambda x: len(x) == 0,
    'count': lambda x: len(x),

    '=':  lambda x,y: general_op(x, y, operator.eq),
    '<':  lambda x,y: general_op(x, y, operator.lt),
    '<=': lambda x,y: general_op(x, y, operator.le),
    '>':  lambda x,y: general_op(x, y, operator.gt),
    '>=': lambda x,y: general_op(x, y, operator.ge),
}
