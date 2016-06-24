
def _escape(s):
    return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')

def pr_str(v, print_readably=False):
    if not hasattr(v, 'type'):
        if v != None:
            raise Exception("pr_str: Error getting a valid type to print(got %s)" % type(v))
        else:
            return

    if v.type == 'symbol':
        return v.symval
    elif v.type == 'num':
        return str(v.num)
    elif v.type == 'str':
        if print_readably:
            return '"%s"' % _escape(v.value)
        else:
            return v.value
    elif v.type == 'nil':
        return 'nil'
    elif v.type == 'bool':
        return str(v.value)
    elif v.type == 'list':
        res = []
        for el in v.values:
            val = pr_str(el, print_readably)
            res.append(val)
        res = ' '.join(res)
        return "(%s)" % res
    elif v.type == 'vec':
        res = []
        for el in v.values:
            val = pr_str(el, print_readably)
            res.append(val)
        res = ' '.join(res)
        return "[%s]" % res
    elif v.type == 'hashmap':
        res = []
        for k in v.hm.keys():
            res.append(pr_str(k))
            res.append(pr_str(v.hm[k], print_readably))
        res = ' '.join(res)
        return "{%s}" % res
    elif v.type == 'function':
        return repr(v)
    else:
        raise Exception("No type found: %s" % v.type)
