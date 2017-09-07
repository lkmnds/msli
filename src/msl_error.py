
debug_flag = True

class MslError(Exception):
    pass

def error(msg):
    raise MslError(msg)

def debug(msg):
    if debug_flag:
        print(msg)

def set_dflag(v):
    global debug_flag
    debug_flag = v
