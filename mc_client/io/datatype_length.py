def boolean_length():
    return 1

def byte_length():
    return 1

def sbyte_length():
    return 1

def short_length():
    return 2

def ushort_length():
    return 2

def int_length():
    return 4

def long_length():
    return 8

def float_length():
    return 4

def double_length():
    return 8

def varint_length(value):
    if value < -0x80000000:
        raise Exception(f'{value} is too small. Expected values between -2147483648 and 2147483647')
    elif value < 0x0:
        return 5
    elif value < 0x80:
        return 1
    elif value < 0x4000:
        return 2
    elif value < 0x200000:
        return 3
    elif value < 0x10000000:
        return 4
    elif value < 0x80000000:
        return 5
    raise Exception(f'{value} is too large. Expected values between -2147483648 and 2147483647')

def varlong_length(value):
    if value < -0x8000000000000000:
        raise Exception(f'{value} is too small. Expected values between -9223372036854775808 and 9223372036854775807')
    elif value < 0x0:
        return 10
    elif value < 0x80:
        return 1
    elif value < 0x4000:
        return 2
    elif value < 0x200000:
        return 3
    elif value < 0x10000000:
        return 4
    elif value < 0x800000000:
        return 5
    elif value < 0x40000000000:
        return 6
    elif value < 0x2000000000000:
        return 7
    elif value < 0x100000000000000:
        return 8
    elif value < 0x8000000000000000:
        return 9
    raise Exception(f'{value} is too large. Expected values between -9223372036854775808 and 9223372036854775807')

def string_length(string):
    encode_length = len(string.encode('utf8'))
    return varint_length(encode_length) + encode_length
