def check_void(args):
    copy = args.copy()
    for key in args:
        if args[key] is None or len(args[key].strip()) == 0:
            del copy[key]
    return copy


def check_len_str(name_arg: str, arg: str, length=0):
    condition = len(arg.strip().split()) > 0 and len(arg.strip().split()) >= length
    if condition:
        return True
    return f'Condition for {name_arg} is {condition}, argument {name_arg} is incomplete'


def check_len_number(name_arg: str, arg: int, length):
    condition = len(str(arg)) == length
    if condition:
        return True
    return f'Condition for {name_arg} is {condition}, length argument {name_arg} != {length}'

