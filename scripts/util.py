

def parse_args(oargs, flags=[], named=[]):
    # copy args so we don't modify the original
    args = [ *oargs ]
    flags_found, named_found = [], []
    
    for f in flags:
        flags_found.append(f in args)
        if flags_found[-1]:
            args.remove(f)
    
    for n in named:
        named_found.append(None)
        if n in args:
            named_found[-1] = args[args.index(n) + 1]
            args.remove(n)
            args.remove(named_found[-1])
    
    return args, flags_found, named_found

