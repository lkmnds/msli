import traceback
import readline
import sys
argv = sys.argv

import msl_reader as reader
import msl_printer as printer

import msl_types as mtypes

enviroment = {
    '+': lambda a,b: a+b,
    '-': lambda a,b: a-b,
    '*': lambda a,b: a*b,
    '/': lambda a,b: a/b,
}

def msl_read(string):
    return reader.read_str(string)

def eval_ast(ast, env):
    if ast.type == 'symbol':
        if ast.symval in env:
            return env[ast.symval]
        else:
            raise Exception("Symbol %s not found" % ast.symval)
    elif ast.type == 'list':
        print('values', ast.values)
        res = []
        for e in ast.values:
            evaled = msl_eval(e, env)
            res.append(evaled)
        print('eval\'', repr(evaled))
        return mtypes.MslList(res)
    else:
        return ast

def msl_eval(ast, env):
    if hasattr(ast, 'type'):
        if ast.type == 'list':
            if len(ast) == 0:
                return ast
            else:
                d = eval_ast(ast, env)
                func = d.values[0]
                fargs = d.values[1:]
                print('fargs', repr(fargs))
                return func(*fargs)
        else:
            return eval_ast(ast, env)
    else:
        return eval_ast(ast, env)
    return ast

def msl_print(exp):
    return printer.pr_str(exp, True)

def msl_rep(string):
    return msl_print(msl_eval(msl_read(string), enviroment))

def main():
    # repl loop
    while True:
        try:
            line = input("msl> ")
            if line == None: break
            if line == "": continue

            print(msl_rep(line))
        except Exception as e:
            print("".join(traceback.format_exception(*sys.exc_info())))

if __name__ == '__main__':
    main()
