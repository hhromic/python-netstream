#pylint: disable=R0911

"""Value encoders for the NetStream protocol."""

import netstream
import struct
import varint

def encode_value(value, dtype):
    """Encode a value according to a given data type."""
    if dtype is netstream.TYPE_BOOLEAN:
        return encode_boolean(value)
    elif dtype is netstream.TYPE_BOOLEAN_ARRAY:
        return encode_boolean_array(value)
    elif dtype is netstream.TYPE_INT:
        return encode_int(value)
    elif dtype is netstream.TYPE_INT_ARRAY:
        return encode_int_array(value)
    elif dtype is netstream.TYPE_LONG:
        return encode_long(value)
    elif dtype is netstream.TYPE_LONG_ARRAY:
        return encode_long_array(value)
    elif dtype is netstream.TYPE_DOUBLE:
        return encode_double(value)
    elif dtype is netstream.TYPE_DOUBLE_ARRAY:
        return encode_double_array(value)
    elif dtype is netstream.TYPE_STRING:
        return encode_string(value)
    raise NotImplementedError("type not supported")

def encode_boolean(value):
    """Encode a boolean type."""
    return bytearray([value & 1])

def encode_boolean_array(value):
    """Encode an array of boolean values."""
    if not isinstance(value, list):
        raise TypeError("value is not an array")
    buff = bytearray()
    buff.extend(varint.encode_unsigned(len(value)))
    for elem in value:
        if not isinstance(elem, bool):
            raise TypeError("array element is not a boolean")
        buff.extend(encode_boolean(elem))
    return buff

def encode_int(value):
    """Encode an integer type."""
    return varint.encode_unsigned(value)

def encode_int_array(value):
    """Encode an array of integer values."""
    if not isinstance(value, list):
        raise TypeError("value is not an array")
    buff = bytearray()
    buff.extend(varint.encode_unsigned(len(value)))
    for elem in value:
        if not isinstance(elem, int):
            raise TypeError("array element is not an integer")
        buff.extend(encode_int(elem))
    return buff

def encode_long(value):
    """Encode a long type."""
    return encode_int(value) # same as int for now

def encode_long_array(value):
    """Encode an array of long values."""
    return encode_int_array(value) # same as int_array for now

def encode_double(value):
    """Encode a double type."""
    return bytearray(struct.pack("!d", value))

def encode_double_array(value):
    """Encode an array of double values."""
    if not isinstance(value, list):
        raise TypeError("value is not an array")
    buff = bytearray()
    buff.extend(varint.encode_unsigned(len(value)))
    for elem in value:
        if not isinstance(elem, float):
            raise TypeError("array element is not a float/double")
        buff.extend(encode_double(elem))
    return buff

def encode_string(string):
    """Encode a string type."""
    data = bytearray(string, "UTF-8")
    buff = bytearray()
    buff.extend(varint.encode_unsigned(len(data)))
    buff.extend(data)
    return buff

def encode_byte(value):
    """Encode a byte type."""
    return bytearray([value])
