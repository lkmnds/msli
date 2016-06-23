
def pr_str(v):
    if type(v) == type([]):
        return 'python list: nope'
    elif v.type == 'str':
        return v
    elif v.type == 'symbol':
        return v.symval
    elif v.type == 'num':
        return str(v.num)
    elif v.type == 'list':
        res = ' '.join(map(pr_str, v.values))
        return "(%s)" % res
