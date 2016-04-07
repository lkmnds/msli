import sys

def evaluate(s):
    def add(a, b): return a+b
    return eval(s)

def main():
    args = sys.argv
    if len(args) > 1:
        with open(args[1], 'r') as f:
            final = generate_code(f.read())
            print(evaluate(final))

if __name__ == '__main__':
    main()
