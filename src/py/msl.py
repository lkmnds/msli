import traceback
import readline
import sys
argv = sys.argv

def msl_read(string):
    return string

def msl_eval(ast, env):
    return ast

def msl_print(exp):
    return exp

def msl_rep(string):
    return msl_print(msl_eval(msl_read(string), {}))

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
