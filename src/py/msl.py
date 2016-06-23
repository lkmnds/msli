import traceback
import readline
import sys
argv = sys.argv

import msl_reader as reader
import msl_printer as printer

def msl_read(string):
    return reader.read_str(string)

def msl_eval(ast, env):
    return ast

def msl_print(exp):
    print(exp)
    return printer.pr_str(exp)

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
