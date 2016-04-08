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
    def __str__(self):
        return str(self.value)
    def __repr__(self):
        return 'Node('+self.type+','+repr(self.value)+':'+str(self.params)+')'

class AST:
    def __init__(self, _type, body):
        self.type = _type
        self.body = []
        self._context = None
    def __repr__(self):
        return 'AST('+str(self.body)+')'

class Expression:
    def __init__(self, _type, callee={}, arguments=[], expression=None):
        self.type = _type
        self.callee = callee
        self.arguments = arguments
        self.expression = expression

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
        elif char == '?':
            tokens.append(Token('sign', '?'))
            i += 1
            continue
        elif char == ',':
            tokens.append(Token('comma', ','))
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
    print(len(tokens))
    def walk():
        nonlocal i
        token = tokens[i]
        if token.type == 'number':
            i += 1
            return Node('NumberLiteral', token.value)
        elif token.type == 'name':
            i += 1
            return Node('Name', token.value)
        elif token.type == 'space':
            i += 1
            return token.value
        elif token.type == 'newline':
            i += 1
            return Node('Newline', token.value)
        elif token.type == 'sign':
            i += 1
            return token.value
        elif token.type == 'string':
            i += 1
            token = tokens[i]
            n = Node('StringExpression', token.value)

            i += 1
            token = tokens[i]
            while token.type != 'string' and token.value != '"':
                n.value += str(walk())
                token = tokens[i]

            i += 1
            return n
        elif token.type == 'paren':
            fname = tokens[i-1] #get identifier
            i += 1
            token = tokens[i] #skip parenthesis
            n = Node('CallExpression', {'name': fname, 'params': [None]})

            while token.type != 'paren' and token.value != ')':
                cp = 0
                if token.type != 'comma':
                    n.value['params'][cp] = walk()
                else:
                    cp += 1
                token = tokens[i]

            i += 1 #close parenthesis
            return n
        else:
            raise Exception("Error parsing token " + repr(token))

    ast = AST('Program', [])

    while i < len(tokens):
        ast.body.append(walk())

    return ast

def traverse(ast, visitor):
    def traverse_array(a, p):
        for e in a:
            traverse_node(e, p)

    def traverse_node(node, parent):
        if node.type in visitor:
            visitor[node.type](node, parent)

        if node.type == 'Program':
            traverse_array(node.body, node)
        elif node.type == 'CallExpression':
            traverse_array(node.value['params'], node)
        elif node.type == 'StringExpression':
            pass
        elif node.type == 'Newline':
            pass
        elif node.type == 'Name':
            pass
        else:
            raise Exception("Error traversing node type " + node.type)

    traverse_node(ast, None)

def transform(ast):
    newAst = AST('Program', [])

    ast._context = newAst.body

    def call_expression(n, p):
        exp = Expression('CallExpression', Node('Identifier', n.value['name']), [])
        n._context = exp.arguments
        if p.type != 'CallExpression':
            exp = Expression('ExpressionStatement', expression=exp)
        p._context.append(exp)

    traverse(ast, {
        'StringExpression': (lambda n, p:
            p._context.append(Node('StringExpression', n.value))
        ),
        'CallExpression': call_expression
    })

    return newAst

def execnode(node):
    if node.type == 'Program':
        for n in node.body:
            execnode(n)
    elif node.type == 'StringExpression':
        return node.value
    elif node.type == 'CallExpression':
        if node.callee == 'echo':
            for n in node.arguments:
                execnode(n)
    elif node.type == 'ExpressionStatement':
        if node.expression.callee.value.value == 'echo':
            print(node.expression.arguments[0])
    elif node.type == 'Identifier':
        return node.name
    elif node.type == 'NumberLiteral':
        return node.value
    else:
        print(node.type)
        raise Exception('Error executing node: ' + repr(node))

def main():
    args = sys.argv
    if len(args) > 1:
        with open(args[1], 'r') as f:
            tokens = tokenize(f.read())
            pprint.pprint(tokens)

            ast = parse(tokens)
            pprint.pprint(ast)

            nAst = transform(ast)
            pprint.pprint(nAst)

            execnode(nAst)

if __name__ == '__main__':
    main()
