import msl_types as mtypes
import re

class Reader:
    def __init__(self, tok):
        self.tokens = tok
        self.position = 0

    def next(self):
        self.position += 1
        return self.tokens[self.position-1]

    def peek(self):
        if len(self.tokens) > self.position:
            return self.tokens[self.position]
        else:
            return None

def tokenize(str):
    tre = re.compile(r"""[\s,]*(~@|[\[\]{}()'`~^@]|"(?:[\\].|[^\\"])*"?|;.*|[^\s\[\]{}()'"`@,;]+)""");
    return [t for t in re.findall(tre, str) if t[0] != ';']

def read_form(reader):
    tok = reader.peek()
    val = None
    if not tok:
        val = mtypes.MslNil()
    elif tok[0] == ';':
        reader.next()
        val = None
    elif tok == '\'':
        reader.next()
        return mtypes.MslList([
            mtypes.MslSymbol('quote'),
            read_form(reader)
        ])
    elif tok == '`':
        reader.next()
        return mtypes.MslList([
            mtypes.MslSymbol('quasiquote'),
            read_form(reader)
        ])
    elif tok == '~':
        reader.next()
        return mtypes.MslList([
            mtypes.MslSymbol('unquote'),
            read_form(reader)
        ])
    elif tok == '~@':
        reader.next()
        return mtypes.MslList([
            mtypes.MslSymbol('slice-unquote'),
            read_form(reader)
        ])

    elif tok == ')':
        raise Exception("Unexpected ')' reading form")
    elif tok == '(':
        val = read_list(reader)

    elif tok == ']':
        raise Exception("Unexpected ']'")
    elif tok == '[':
        val = read_vector(reader)

    elif tok == '}':
        raise Exception("Unexpected '}'")
    elif tok == '{':
        val = read_hashmap(reader)

    else:
        print("get atom %s" % reader.peek())
        val = read_atom(reader)

    return val

def read_seq(reader, start='(', end=')', init=mtypes.MslList):
    ast = init([])
    token = reader.next()
    if token != start: raise Exception("Unexpected %s reading sequence" % token)

    token = reader.peek()

    while token != end:
        if not token:
            raise Exception("Expected '%s', got EOF" % end)
        token_form = read_form(reader)
        ast.append(token_form)
        print("append token", token_form)
        token = reader.peek()

    return ast

def read_vector(reader):
    return read_seq(reader, '[', ']', mtypes.MslVector)

def read_hashmap(reader):
    lst = read_seq(reader, '{', '}', list)
    return mtypes.MslHashmap(lst)

def read_list(reader):
    return read_seq(reader)

def _unescape(s):
    return s.replace('\\"', '"').replace('\\n', '\n').replace('\\\\', '\\')

def read_atom(reader):
    int_re = re.compile(r"-?[0-9]+$")
    float_re = re.compile(r"-?[0-9][0-9.]*$")
    token = reader.next()

    if re.match(int_re, token):
        return mtypes.MslNumber(token)
    elif re.match(float_re, token):
        return mtypes.MslNumber(token)
    elif token[0] == '"':
        if token[-1] == '"':
            return mtypes.MslStr(_unescape(token[1:-1]))
        else:
            raise Exception("Expected '\"', got EOF")
    elif token[0] == ':':
        return mtypes.MslKeyword(token[1:])
    elif token == 'nil':
        return mtypes.MslNil()
    elif token == 'true':
        return mtypes.MslBool(True)
    elif token == 'false':
        return mtypes.MslBool(False)
    else:
        return mtypes.MslSymbol(token)

def read_str(string):
    ast = []
    return read_form(Reader(tokenize(string)))
