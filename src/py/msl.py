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

def msl_read(string):
    return reader.read_str(string)

def eval_ast(ast, env):
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

                    elif funcname == 'exit' or funcname == 'quit':
                        a1 = ast.values[1]
                        if not isinstance(a1, mtypes.MslNumber):
                            raise Exception("A number is required")
                        sys.exit(a1.num)

                    elif funcname == 'do':
                        eval_ast(ast.values[1:-1], env)
                        ast = ast[-1]

                    elif funcname == 'if':
                        a1 = ast.values[1]
                        ret = msl_eval(a1, env)

                        cond = msl_eval(a1, env)
                        if cond is None or cond is False:
                            if len(ast.values) > 3:
                                ast = ast.values[3]
                            else:
                                ast = None
                        else:
                            ast = ast.values[2]

                    elif funcname == 'fn*':
                        a1, a2 = ast.values[1], ast.values[2]
                        return mtypes.MslFunction(msl_eval, menv.Enviroment, a2, env, a1)

                    else:
                        d = eval_ast(ast, env)
                        f = d[0]

                        print(f)

                        if hasattr(f, '__ast__'):
                            print("got __ast__ func")
                            ast = f.__ast__
                            env = f.__gen__env(d.values[1:])
                        else:
                            return f(*d.values[1:])

                        '''
                        if hasattr(funcname, 'type'):
                            if funcname.type == 'function':
                                # function call(maybe?)
                                func_call = funcname
                            elif funcname.type == 'list':
                                # got lambda
                                func_call = msl_eval(funcname, env)
                                func_type = 'decl'
                            else:
                                # just as usual, get from the env
                                func_call = envfunc.get(funcname)
                        else:
                            func_call = envfunc.get(funcname)

                        if func_call == None:
                            raise Exception("No function %s found" % funcname)

                        return func_call(*fargs)
                        '''
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

def msl_rep(string):
    return msl_print(msl_eval(msl_read(string), repl_env))

def main():
    # repl loop
    global hist_loaded

    print("msl v%s b%d" % (mtypes.MSL_VERSION, mtypes.MSL_BUILD))

    path = (os.path.realpath(__file__)).split('/')
    initmsl = "%s/msllib/init.msl" % '/'.join(path[:-1])
    with open(initmsl, 'r') as fh:
        for line in fh.readlines():
            msl_rep(line)

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
