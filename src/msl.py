import traceback
import readline
import sys
argv = sys.argv
import os
import os.path

import msl_reader as reader
import msl_printer as printer

import msl_types as mtypes
import msl_env as menv
import msl_core as mcore
import msl_error as merror

hist_loaded = False
hist_file = os.path.expanduser("~/.msl-history")

def is_pair(x):
    if hasattr(x, 'type'):
        if isinstance(x, mtypes.MslList):
            return len(x) != 0
    elif isinstance(x, list):
        return len(x) != 0
    else:
        return False

def quasiquote(ast, qflag=False):
    print("qquote", ast)
    if not is_pair(ast):
        if isinstance(ast, mtypes.MslList):
            if len(ast) > 0:
                return ast[0]
            else:
                return ast
        else:
            if isinstance(ast, mtypes.MslSymbol):
                return mtypes.MslList([
                    mtypes.MslSymbol("quote"),
                    ast
                ])
            else:
                return ast

    elif ast[0] == mtypes.MslSymbol('unquote'):
        return ast[1]

    elif is_pair(ast[0]) and ast[0][0] == mtypes.MslSymbol('splice-unquote'):
        if len(ast[1:]) > 0:
            lst = [
                mtypes.MslSymbol("concat"),
                ast[0][1],
            ]
            lst.append(quasiquote(ast[1:]))
            return mtypes.MslList(lst)
        else:
            lst = [
                ast[0][1],
            ]
            return mtypes.MslList(lst)

    else:
        if len(ast[1:]) > 0:
            lst = [
                mtypes.MslSymbol("cons"),
                quasiquote(ast[0]),
            ]
            lst.append(quasiquote(ast[1:], True))

            return mtypes.MslList(lst)
        else:
            lst = [
                quasiquote(ast[0], True),
            ]
            return mtypes.MslList(lst)

def msl_read(string):
    return reader.read_str(string)

def eval_ast(ast, env):
    if not hasattr(ast, 'type'):
        merror.error("eval_ast: Error evaluating AST(%s) %s" % (type(ast), repr(ast)))

    if ast.type == 'symbol':
        return env.get(ast.symval)
    elif ast.type == 'list':
        res = []
        for e in ast.values:
            evaled = msl_eval(e, env)
            res.append(evaled)
        return mtypes.MslList(res)
    elif ast.type == 'vec':
        res = []
        for e in ast.values:
            evaled = msl_eval(e, env)
            res.append(evaled)
        return mtypes.MslVector(res)
    elif ast.type == 'hashmap':
        newhm = mtypes.MslHashmap([])
        for k in ast.hm:
            newhm.hm[k] = msl_eval(ast.hm[k], env)
        return newhm
    else:
        return ast

def msl_eval(ast, env):
    while True:
        # print('ast', repr(ast))
        if hasattr(ast, 'type'):
            if ast.type == 'list':
                if len(ast) == 0:
                    return ast
                else:
                    funcname = ast.values[0]

                    if hasattr(funcname, 'type'):
                        if funcname.type == 'symbol':
                            funcname = funcname.symval

                    if funcname == 'def!':
                        a1, a2 = ast.values[1], ast.values[2]
                        res = msl_eval(a2, env)
                        return env.set(a1.symval, res)

                    elif funcname == "let*":
                        a1, a2 = ast.values[1], ast.values[2]
                        let_env = menv.Enviroment(env)

                        for i in range(0, len(a1), 2):
                            let_env.set(a1.values[i].symval, msl_eval(a1.values[i+1], let_env))
                        env = let_env
                        ast = a2
                        continue

                    elif funcname == 'exit' or funcname == 'quit':
                        a1 = ast.values[1]
                        if not isinstance(a1, mtypes.MslNumber):
                            raise RuntimeError('A number is required')
                        sys.exit(a1.num)

                    elif funcname == 'do':
                        vals = mtypes.MslList(ast.values[1:-1])
                        eval_ast(vals, env)
                        ast = ast[-1]
                        continue

                    elif funcname == 'if':
                        a1, a2 = ast.values[1], ast.values[2]

                        cond = msl_eval(a1, env)

                        if (cond == None) or (not cond):
                            if len(ast.values) > 3:
                                ast = ast.values[3]
                                continue
                            else:
                                ast = None
                                continue
                        else:
                            ast = a2
                            continue

                    elif funcname == 'fn*':
                        a1, a2 = ast.values[1], ast.values[2]
                        return mtypes.MslFunction(msl_eval, menv.Enviroment, a2, env, a1)

                    elif funcname == 'quote':
                        return ast.values[1]

                    elif funcname == 'quasiquote':
                        ast = quasiquote(ast[1], False)
                        continue

                    else:
                        d = eval_ast(ast, env)
                        f = d[0]

                        if hasattr(f, '__ast__'):
                            ast = f.__ast__
                            env = f.__gen__env(d.values[1:])
                            continue
                        else:
                            if callable(f):
                                return f(*d.values[1:])
            # my beautiful hack
            elif isinstance(ast, mtypes.MslPList):
                possible_fname = ast[0]

                print('pfname', possible_fname)

                '''
                TODO:

                msl> `(1 2 (3 4))
                pfname List([Symbol('cons'), Number(3), P_List([Number(4)])])
                pfname Number(4)
                (1 2 3 4)

                should give (1 2 (3 4))

                '''

                if isinstance(possible_fname, mtypes.MslList):
                    if isinstance(possible_fname[0], mtypes.MslSymbol):
                        if env.find(possible_fname[0].symval):
                            '''print("got func %s in plist" % possible_fname[0].symval)
                            print("fargs %r" % possible_fname[1:])'''

                            d = eval_ast(possible_fname, env)
                            f = d[0]
                            # ast = mtypes.MslList(ast.values)
                            return f(*d.values[1:])
            else:
                return eval_ast(ast, env)
        else:
            return eval_ast(ast, env)
        return ast

def msl_print(exp):
    return printer.pr_str(exp, True)

repl_env = menv.Enviroment()
for key in mcore.ns:
    repl_env.set(key, mcore.ns[key])

repl_env.set('eval', lambda ast: msl_eval(ast, repl_env))
repl_env.set('*ARGV*', sys.argv[2:])

def msl_rep(string):
    try:
        return msl_print(msl_eval(msl_read(string), repl_env))
    except RuntimeError as e:
        merror.error("Runtime Error: %s" % str(e))

def main():
    # repl loop
    global hist_loaded

    print(f'msl {mtypes.MSL_VERSION} build {mtypes.MSL_BUILD}')

    path = (os.path.realpath(__file__)).split('/')

    stdlib_list = [
        'init',
        'math',
    ]
    stdlib = [f"{'/'.join(path[:-1])}/msllib/{libname}.msl" for libname in stdlib_list]

    # read the standard lib
    for fpath in stdlib:
        with open(fpath, 'r') as fh:
            for line in fh.readlines():
                msl_rep(reader._unescape(line))

    if len(argv) < 2:
        # start REPL
        while True:
            try:
                if not hist_loaded:
                    hist_loaded = True
                    try:
                        with open(hist_file, 'r') as hf:
                            for line in hf.readlines():
                                readline.add_history(line.rstrip("\r\n"))
                    except IOError:
                        pass
                line = input("msl> ")
                readline.add_history(line)

                with open(hist_file, 'a') as hf:
                    hf.write(line + '\n')
                if line == None: break
                if line == "": continue

                print(msl_rep(line))
            except Exception as e:
                print("".join(traceback.format_exception(*sys.exc_info())))
    else:
        filename = argv[1]
        filename = os.path.realpath(filename)
        with open(filename, 'r') as fh:
            for line in fh.readlines():
                print(msl_rep(line))

if __name__ == '__main__':
    main()
