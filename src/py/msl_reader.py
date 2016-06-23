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
    if tok == '(':
        val = read_list(reader)
    else:
        val = read_atom(reader)

    return val

def read_seq(reader, start='(', end=')'):
    ast = mtypes.MslList([])
    token = reader.next()
    if token != start: raise Exception("Unexpected %s" % token)

    token = reader.peek()

    while token != end:
        if not token:
            raise Exception("Expected '%s', got EOF" % end)
        ast.values.append(read_form(reader))
        token = reader.peek()

    return ast

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
