def check_void(args):
    copy = args.copy()
    for key in args:
        if args[key] is None or len(args[key].strip()) == 0:
            del copy[key]
    return copy
