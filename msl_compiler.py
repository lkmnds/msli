import sys
import pprint
import time

class Token:
    def __init__(self, _type, value):
        self.type = _type
        self.value = value
    def __repr__(self):
        return 'Token('+self.type+','+repr(self.value)+')'

class Node:
    def __init__(self, _type, value, params=[]):
        self.type = _type
        self.value = value
        self.params = params
        def __repr__(self):
            return 'Node('+self.type+','+repr(self.value)+':'+self.params+')'

class AST:
    def __init__(self, _type, body):
        self.type = _type
        self.body = []
    def __repr__(self):
        return 'AST('+self.body+')'

def tokenize(s):
    i = 0
    tokens = []
    while i < len(s):
        char = s[i]
        if char == '"': #starting or ending strings
            tokens.append(Token('string', '"'))
            i += 1
            continue
        elif char == '(':
            tokens.append(Token('paren', '('))
            i += 1
            continue
        elif char == ')':
            tokens.append(Token('paren', ')'))
            i += 1
            continue
        elif char == ';':
            tokens.append(Token('semicolon', ';'))
            i += 1
            continue
        elif char == ' ':
            tokens.append(Token('space', ' '))
            i += 1
            continue
        elif char == '\n':
            tokens.append(Token('newline', '\n'))
            i += 1
            continue
        elif char.isnumeric():
            v = ''
            while char.isnumeric():
                v += char
                i += 1
                char = s[i]
            tokens.append(Token('number', v))
            continue
        elif char.isalpha():
            v = ''
            while char.isalpha():
                v += char
                i += 1
                char = s[i]
            tokens.append(Token('name', v))
            continue
        else:
            raise Exception("Unexpected character: '" + char + "'")
    return tokens

def parse(tokens):
    i = 0
    ast = AST('Program', [])
    def walk():
        print("ualkque")
        nonlocal i
        token = tokens[i]
        if token.type == 'number':
            i += 1
            return Node('NumberLiteral', token.value)
        elif token.type == 'name':
            i += 1
            return token.value
        elif token.type == 'space':
            i += 1
            return token.value
        elif token.type == 'newline':
            i += 1
            return token.value
        elif token.type == 'string':
            print("str")
            i += 1
            token = tokens[i]
            print(token)
            n = Node('StringExpr', token.value)

            i += 1
            token = tokens[i]
            while token.type != 'string' and token.value != '"':
                print(token)
                n.value += (walk())
                token = tokens[i]

            i += 1
            return n
        else:
            raise Exception("Error parsing token " + repr(token))

    while i < len(tokens):
        ast.body.append(walk())

    return ast

def traverse(ast, visitor):
    pass

def transform(ast):
    pass

def execute(ast):
    i = 0
    program_cache = []

def main():
    args = sys.argv
    if len(args) > 1:
        with open(args[1], 'r') as f:
            tokens = tokenize(f.read())
            pprint.pprint(tokens)

            ast = parse(tokens)
            pprint.pprint(ast)

            nAst = transform(ast)
            execute(nAst)

if __name__ == '__main__':
    main()
