
import msl_printer as printer
import msl_reader as reader

import msl_types as mtypes

import operator

def treat(x):
    if not hasattr(x, 'type'):
        x = mtypes.py_to_msl(x)
    return x

def make_list(*args):
    return mtypes.MslList(args)

def c_pr_str(*args):
    return " ".join(map(lambda exp: printer.pr_str(exp, True), args))

def c_str(*args):
    return "".join(map(lambda exp: printer.pr_str(exp, False), args))

def c_prn(*args):
    print(" ".join(map(lambda exp: printer.pr_str(exp, True), args)))
    return mtypes.MslNil()

def c_println(*args):
    print(" ".join(map(lambda exp: printer.pr_str(exp, False), args)))
    return mtypes.MslNil()

def c_slurp(fname):
    res = ''
    with open(fname) as f:
        res = f.read()
    return mtypes.MslStr(res)

# atom functions
def c_swap(atom, f, *args):
    print(repr(f), atom.value, args)
    atom.value = f(atom.value, *args)
    return atom.value

def c_reset(atom, v):
    atom.value = v
    return v

def c_cons(x, y):
    newlist = mtypes.MslList([])
    newlist.append(x)
    if isinstance(y, mtypes.MslList):
        #newlist.values.extend(y.values)
        newlist.extend(y)
    else:
        newlist.append(y)
    return newlist

def c_concat(*args):
    final_lst = mtypes.MslList([])
    for lst in args:
        final_lst.values.extend(lst)
    return final_lst

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

def cmp_type(x, t):
    if not hasattr(x, 'type'):
        x = mtypes.py_to_msl(x)
    return isinstance(x, t)

ns = {
    # Maths.
    '+': lambda x,y: general_op(x, y, operator.add),
    '-': lambda x,y: general_op(x, y, operator.sub),
    '/': lambda x,y: general_op(x, y, operator.truediv),
    '*': lambda x,y: general_op(x, y, operator.mul),

    # step3 functions
    'list': make_list,
    'list?': lambda x: cmp_type(x, mtypes.MslList),
    'empty?': lambda x: len(treat(x)) == 0,
    'count': lambda x: len(treat(x)),

    # string functions
    'pr-str': c_pr_str,
    'str': c_str,
    'prn': c_prn,
    'println': c_println,

    'read-string': reader.read_str,
    'slurp': c_slurp,

    'atom': lambda x: mtypes.MslAtom(x),
    'atom?': lambda x: isinstance(x, mtypes.MslAtom),
    'deref': lambda atom: atom.value,
    'reset!': c_reset,
    'swap!': c_swap,

    'cons': c_cons,
    'concat': c_concat,

    # bool comparators
    '=':  lambda x,y: general_op(x, y, operator.eq),
    '<':  lambda x,y: general_op(x, y, operator.lt),
    '<=': lambda x,y: general_op(x, y, operator.le),
    '>':  lambda x,y: general_op(x, y, operator.gt),
    '>=': lambda x,y: general_op(x, y, operator.ge),
}
