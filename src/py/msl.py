import traceback
import readline
import sys
argv = sys.argv
import os

import msl_reader as reader
import msl_printer as printer

import msl_types as mtypes
import msl_env as menv

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
    if hasattr(ast, 'type'):
        if ast.type == 'list':
            if len(ast) == 0:
                return ast
            else:
                funcname = ast.values[0]

                if hasattr(funcname, 'type'):
                    if funcname.type == 'symbol':
                        funcname = funcname.symval

                print('fname', repr(funcname))

                if funcname == 'def!':
                    a1, a2 = ast.values[1], ast.values[2]
                    res = msl_eval(a2, env)
                    return env.set(a1.symval, res)

                elif funcname == "let*":
                    a1, a2 = ast.values[1], ast.values[2]
                    let_env = menv.Enviroment(env)

                    for i in range(0, len(a1), 2):
                        let_env.set(a1.values[i].symval, msl_eval(a1.values[i+1], let_env))
                    return msl_eval(a2, let_env)

                elif funcname == 'exit' or funcname == 'quit':
                    a1 = ast.values[1]
                    if not isinstance(a1, mtypes.MslNumber):
                        raise Exception("A number is required")
                    sys.exit(a1.num)

                elif funcname == 'do':
                    vals = mtypes.MslList(ast.values[1:])
                    return eval_ast(vals, env).values[-1]

                elif funcname == 'if':
                    a1 = ast.values[1]
                    ret = eval_ast(a1, env)

                    true_condition = ast.values[2]
                    false_condition = None
                    if len(ast.values) > 3:
                        false_condition = ast.values[3]

                    if ret:
                        return msl_eval(true_condition, env)
                    else:
                        if false_condition:
                            return msl_eval(false_condition, env)
                        else:
                            return None

                elif funcname == 'fn*':
                    a1, a2 = ast.values[1], ast.values[2]
                    return mtypes.MslFunction(msl_eval, menv.Enviroment, a2, env, a1)

                else:
                    d = eval_ast(ast, env)
                    fargs = d.values[1:]
                    envfunc = env.find(funcname)
                    return envfunc.get(funcname)(*fargs)
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
    global hist_loaded
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

if __name__ == '__main__':
    main()
