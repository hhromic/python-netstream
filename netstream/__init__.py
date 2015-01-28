#pylint: disable=R0911

"""NetStream implementation for Python to communicate with GraphStream."""

# Package classes
from transports import BinaryNetStreamTransport
from sender import NetStreamSender, NetStreamProxyGraph

# Event codes constants
EVENT_GETVERSION = 0x00
EVENT_START = 0x01
EVENT_END = 0x02
EVENT_ADD_NODE = 0x10
EVENT_DEL_NODE = 0x11
EVENT_ADD_EDGE = 0x12
EVENT_DEL_EDGE = 0x13
EVENT_STEP = 0x14
EVENT_CLEARED = 0x15
EVENT_ADD_GRAPH_ATTR = 0x16
EVENT_CHG_GRAPH_ATTR = 0x17
EVENT_DEL_GRAPH_ATTR = 0x18
EVENT_ADD_NODE_ATTR = 0x19
EVENT_CHG_NODE_ATTR = 0x1A
EVENT_DEL_NODE_ATTR = 0x1B
EVENT_ADD_EDGE_ATTR = 0x1C
EVENT_CHG_EDGE_ATTR = 0x1D
EVENT_DEL_EDGE_ATTR = 0x1E

# Value type codes constants
TYPE_BOOLEAN = 0x50
TYPE_BOOLEAN_ARRAY = 0x51
TYPE_BYTE = 0x52
TYPE_BYTE_ARRAY = 0x53
TYPE_SHORT = 0x54
TYPE_SHORT_ARRAY = 0x55
TYPE_INT = 0x56
TYPE_INT_ARRAY = 0x57
TYPE_LONG = 0x58
TYPE_LONG_ARRAY = 0x59
TYPE_FLOAT = 0x5A
TYPE_FLOAT_ARRAY = 0x5B
TYPE_DOUBLE = 0x5C
TYPE_DOUBLE_ARRAY = 0x5D
TYPE_STRING = 0x5E
TYPE_RAW = 0x5F
TYPE_ARRAY = 0x60

# Package functions
def typeof(value):
    """Get the data type for a given value."""
    is_array = isinstance(value, list)
    if is_array:
        value = value[0]
    if isinstance(value, bool):
        if is_array:
            return TYPE_BOOLEAN_ARRAY
        return TYPE_BOOLEAN
    elif isinstance(value, int):
        if is_array:
            return TYPE_INT_ARRAY
        return TYPE_INT
    elif isinstance(value, long):
        if is_array:
            return TYPE_LONG_ARRAY
        return TYPE_LONG
    elif isinstance(value, float):
        if is_array:
            return TYPE_DOUBLE_ARRAY
        return TYPE_DOUBLE
    elif isinstance(value, str) or isinstance(value, unicode):
        return TYPE_STRING
    raise NotImplementedError("type not supported")
