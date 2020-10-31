import struct

def parse_nbt(read_buffer):
    tag_id = read_buffer.read_byte()
    name = read_name(read_buffer)
    return {name:parse(tag_id, read_buffer)}

def read_name(read_buffer):
    length = read_buffer.read_ushort()
    string = read_buffer.read(length).decode('utf8')
    return string

def parse(tag_id, read_buffer):
    if tag_id == 0:
        return None
    elif tag_id == 1:
        return parse_byte(read_buffer)
    elif tag_id == 2:
        return parse_short(read_buffer)
    elif tag_id == 3:
        return parse_int(read_buffer)
    elif tag_id == 4:
        return parse_long(read_buffer)
    elif tag_id == 5:
        return parse_float(read_buffer)
    elif tag_id == 6:
        return parse_double(read_buffer)
    elif tag_id == 7:
        return parse_byte_array(read_buffer)
    elif tag_id == 8:
        return parse_string(read_buffer)
    elif tag_id == 9:
        return parse_list(read_buffer)
    elif tag_id == 10:
        return parse_compound(read_buffer)
    elif tag_id == 11:
        return parse_int_array(read_buffer)
    elif tag_id == 12:
        return parse_long_array(read_buffer)
    else:
        raise Exception('Invalid tag id')

def parse_byte(read_buffer):
    payload = read_buffer.read_sbyte()
    return payload

def parse_short(read_buffer):
    payload = read_buffer.read_short()
    return payload

def parse_int(read_buffer):
    payload = read_buffer.read_int()
    return payload

def parse_long(read_buffer):
    payload = read_buffer.read_long()
    return payload

def parse_float(read_buffer):
    payload = read_buffer.read_float()
    return payload

def parse_double(read_buffer):
    payload = read_buffer.read_double()
    return payload

def parse_byte_array(read_buffer):
    length = read_buffer.read_int()
    payload = [read_buffer.read_sbyte() for _ in range(length)]
    return payload

def parse_string(read_buffer):
    length = read_buffer.read_ushort()
    payload = read_buffer.read(length).decode('utf8')
    return payload

def parse_list(read_buffer):
    tag_id = read_buffer.read_byte()
    length = read_buffer.read_int()
    if length > 0 and tag_id == 0:
        raise Exception("Cannot have a non-zero length list of End Tags")
    if tag_id == 0:
        return []
    else:
        return [parse(tag_id, read_buffer) for _ in range(length)]

def parse_compound(read_buffer):
    tag_id = read_buffer.read_byte()
    output = []
    while tag_id != 0:
        name = read_name(read_buffer)
        payload = parse(tag_id, read_buffer)
        output.append({name:payload})
        tag_id = read_buffer.read_byte()
    return output

def parse_int_array(read_buffer):
    length = read_buffer.read_int()
    return [read_buffer.read_int() for _ in range(length)]

def parse_long_array(read_buffer):
    length = read_buffer.read_int()
    return [read_buffer.read_long() for _ in range(length)]