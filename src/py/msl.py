import traceback
import readline
import sys
argv = sys.argv

import msl_reader as reader
import msl_printer as printer

import msl_types as mtypes
import msl_env as menv

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
    if hasattr(ast, 'type'):
        if ast.type == 'list':
            if len(ast) == 0:
                return ast
            else:
                funcname = ast.values[0]

                if funcname.symval == 'def!':
                    a1, a2 = ast.values[1], ast.values[2]
                    res = msl_eval(a2, env)
                    return env.set(a1.symval, res)

                elif funcname.symval == "let*":
                    a1, a2 = ast.values[1], ast.values[2]
                    let_env = menv.Enviroment(env)

                    for i in range(0, len(a1), 2):
                        let_env.set(a1.values[i].symval, msl_eval(a1.values[i+1], let_env))
                    return msl_eval(a2, let_env)

                elif funcname.symval == 'exit' or funcname.symval == 'quit':
                    a1 = ast.values[1]
                    if not isinstance(a1, mtypes.MslNumber):
                        raise Exception("A number is required")
                    sys.exit(a1.num)

                elif funcname.symval == 'do':
                    vals = mtypes.MslList(ast.values[1:])
                    return eval_ast(vals, env).values[-1]

                elif funcname.symval == 'if':
                    pass

                elif funcname.symval == 'fn*':
                    pass

                else:
                    d = eval_ast(ast, env)
                    fargs = d.values[1:]
                    envfunc = env.find(funcname.symval)
                    return envfunc.get(funcname.symval)(*fargs)
        else:
            return eval_ast(ast, env)
    else:
        return eval_ast(ast, env)
    return ast

def msl_print(exp):
    return printer.pr_str(exp, True)

repl_env = menv.Enviroment()
repl_env.set("+", lambda x,y: x+y)
repl_env.set("-", lambda x,y: x-y)
repl_env.set("*", lambda x,y: x*y)
repl_env.set("/", lambda x,y: x/y)

def msl_rep(string):
    return msl_print(msl_eval(msl_read(string), repl_env))

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
