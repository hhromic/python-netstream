#pylint: disable=R0913,C0301

"""NetStream sending classes."""

import netstream
import encoders
import struct
import random
import logging

class NetStreamSender(object):
    """Sender (sink) to send graph events to a remote server."""

    def __init__(self, transport, stream_id="default"):
        """Initialise using transport and an optional stream ID."""
        self.transport = transport
        self.stream_id = None
        self.stream_id_buff = None
        self.stream_id_length = 0
        self.set_stream_id(stream_id)
        self.transport.connect()

    def set_stream_id(self, stream_id):
        """Set and cache the stream ID for this sender."""
        self.stream_id = stream_id
        self.stream_id_buff = encoders.encode_string(self.stream_id)
        self.stream_id_length = len(self.stream_id_buff)

    def send_event(self, event):
        """Send a graph event to the remote server."""
        buff = bytearray()
        buff.extend(struct.pack("!i", self.stream_id_length + len(event)))
        buff.extend(self.stream_id_buff)
        buff.extend(event)
        self.transport.send(buff)

    def node_added(self, source_id, time_id, node_id):
        """A node was added."""
        buff = bytearray()
        buff.extend(encoders.encode_byte(netstream.EVENT_ADD_NODE))
        buff.extend(source_id)
        buff.extend(encoders.encode_long(time_id))
        buff.extend(encoders.encode_string(node_id))
        self.send_event(buff)
        logging.debug("node added: %s", {
            "source_id": source_id,
            "time_id": time_id,
            "node_id": node_id
        })

    def node_removed(self, source_id, time_id, node_id):
        """A node was removed."""
        buff = bytearray()
        buff.extend(encoders.encode_byte(netstream.EVENT_DEL_NODE))
        buff.extend(source_id)
        buff.extend(encoders.encode_long(time_id))
        buff.extend(encoders.encode_string(node_id))
        self.send_event(buff)
        logging.debug("node removed: %s", {
            "source_id": source_id,
            "time_id": time_id,
            "node_id": node_id
        })

    def edge_added(self, source_id, time_id, edge_id, from_node, to_node, directed):
        """An edge was added."""
        buff = bytearray()
        buff.extend(encoders.encode_byte(netstream.EVENT_ADD_EDGE))
        buff.extend(source_id)
        buff.extend(encoders.encode_long(time_id))
        buff.extend(encoders.encode_string(edge_id))
        buff.extend(encoders.encode_string(from_node))
        buff.extend(encoders.encode_string(to_node))
        buff.extend(encoders.encode_boolean(directed))
        self.send_event(buff)
        logging.debug("edge added: %s", {
            "source_id": source_id,
            "time_id": time_id,
            "edge_id": edge_id,
            "from_node": from_node,
            "to_node": to_node,
            "directed": directed
        })

    def edge_removed(self, source_id, time_id, edge_id):
        """An edge was removed."""
        buff = bytearray()
        buff.extend(encoders.encode_byte(netstream.EVENT_DEL_EDGE))
        buff.extend(source_id)
        buff.extend(encoders.encode_long(time_id))
        buff.extend(encoders.encode_string(edge_id))
        self.send_event(buff)
        logging.debug("edge removed: %s", {
            "source_id": source_id,
            "time_id": time_id,
            "node_id": edge_id
        })

    def step_begun(self, source_id, time_id, timestamp):
        """A new step begun."""
        buff = bytearray()
        buff.extend(encoders.encode_byte(netstream.EVENT_STEP))
        buff.extend(source_id)
        buff.extend(encoders.encode_long(time_id))
        buff.extend(encoders.encode_double(timestamp))
        self.send_event(buff)
        logging.debug("step begun: %s", {
            "source_id": source_id,
            "time_id": time_id,
            "timestamp": timestamp
        })

    def graph_cleared(self, source_id, time_id):
        """The graph was cleared."""
        buff = bytearray()
        buff.extend(encoders.encode_byte(netstream.EVENT_CLEARED))
        buff.extend(source_id)
        buff.extend(encoders.encode_long(time_id))
        self.send_event(buff)
        logging.debug("graph cleared: %s", {
            "source_id": source_id,
            "time_id": time_id
        })

    def graph_attr_added(self, source_id, time_id, attr, value):
        """A graph attribute was added."""
        buff = bytearray()
        buff.extend(encoders.encode_byte(netstream.EVENT_ADD_GRAPH_ATTR))
        buff.extend(source_id)
        buff.extend(encoders.encode_long(time_id))
        buff.extend(encoders.encode_string(attr))
        dtype = netstream.typeof(value)
        buff.extend(encoders.encode_byte(dtype))
        buff.extend(encoders.encode_value(value, dtype))
        self.send_event(buff)
        logging.debug("graph attribute added: %s", {
            "source_id": source_id,
            "time_id": time_id,
            "attr": attr,
            "value": value
        })

    def graph_attr_changed(self, source_id, time_id, attr, old_value, new_value):
        """A graph attribute was changed."""
        buff = bytearray()
        buff.extend(encoders.encode_byte(netstream.EVENT_CHG_GRAPH_ATTR))
        buff.extend(source_id)
        buff.extend(encoders.encode_long(time_id))
        buff.extend(encoders.encode_string(attr))
        dtype = netstream.typeof(old_value)
        buff.extend(encoders.encode_byte(dtype))
        buff.extend(encoders.encode_value(old_value, dtype))
        dtype = netstream.typeof(new_value)
        buff.extend(encoders.encode_byte(dtype))
        buff.extend(encoders.encode_value(new_value, dtype))
        self.send_event(buff)
        logging.debug("graph attribute changed: %s", {
            "source_id": source_id,
            "time_id": time_id,
            "attr": attr,
            "old_value": old_value,
            "new_value": new_value
        })

    def graph_attr_removed(self, source_id, time_id, attr):
        """A graph attribute was removed."""
        buff = bytearray()
        buff.extend(encoders.encode_byte(netstream.EVENT_DEL_GRAPH_ATTR))
        buff.extend(source_id)
        buff.extend(encoders.encode_long(time_id))
        buff.extend(encoders.encode_string(attr))
        self.send_event(buff)
        logging.debug("graph attribute removed: %s", {
            "source_id": source_id,
            "time_id": time_id,
            "attr": attr
        })

    def node_attr_added(self, source_id, time_id, node_id, attr, value):
        """A node attribute was added."""
        buff = bytearray()
        buff.extend(encoders.encode_byte(netstream.EVENT_ADD_NODE_ATTR))
        buff.extend(source_id)
        buff.extend(encoders.encode_long(time_id))
        buff.extend(encoders.encode_string(node_id))
        buff.extend(encoders.encode_string(attr))
        dtype = netstream.typeof(value)
        buff.extend(encoders.encode_byte(dtype))
        buff.extend(encoders.encode_value(value, dtype))
        self.send_event(buff)
        logging.debug("node attribute added: %s", {
            "source_id": source_id,
            "time_id": time_id,
            "node_id": node_id,
            "attr": attr,
            "value": value
        })

    def node_attr_changed(self, source_id, time_id, node_id, attr, old_value, new_value):
        """A node attribute was changed."""
        buff = bytearray()
        buff.extend(encoders.encode_byte(netstream.EVENT_CHG_NODE_ATTR))
        buff.extend(source_id)
        buff.extend(encoders.encode_long(time_id))
        buff.extend(encoders.encode_string(node_id))
        buff.extend(encoders.encode_string(attr))
        dtype = netstream.typeof(old_value)
        buff.extend(encoders.encode_byte(dtype))
        buff.extend(encoders.encode_value(old_value, dtype))
        dtype = netstream.typeof(new_value)
        buff.extend(encoders.encode_byte(dtype))
        buff.extend(encoders.encode_value(new_value, dtype))
        self.send_event(buff)
        logging.debug("node attribute changed: %s", {
            "source_id": source_id,
            "time_id": time_id,
            "node_id": node_id,
            "attr": attr,
            "old_value": old_value,
            "new_value": new_value
        })

    def node_attr_removed(self, source_id, time_id, node_id, attr):
        """A node attribute was removed."""
        buff = bytearray()
        buff.extend(encoders.encode_byte(netstream.EVENT_DEL_NODE_ATTR))
        buff.extend(source_id)
        buff.extend(encoders.encode_long(time_id))
        buff.extend(encoders.encode_string(node_id))
        buff.extend(encoders.encode_string(attr))
        self.send_event(buff)
        logging.debug("node attribute removed: %s", {
            "source_id": source_id,
            "time_id": time_id,
            "node_id": node_id,
            "attr": attr
        })

    def edge_attr_added(self, source_id, time_id, edge_id, attr, value):
        """An edge attribute was added."""
        buff = bytearray()
        buff.extend(encoders.encode_byte(netstream.EVENT_ADD_EDGE_ATTR))
        buff.extend(source_id)
        buff.extend(encoders.encode_long(time_id))
        buff.extend(encoders.encode_string(edge_id))
        buff.extend(encoders.encode_string(attr))
        dtype = netstream.typeof(value)
        buff.extend(encoders.encode_byte(dtype))
        buff.extend(encoders.encode_value(value, dtype))
        self.send_event(buff)
        logging.debug("edge attribute added: %s", {
            "source_id": source_id,
            "time_id": time_id,
            "edge_id": edge_id,
            "attr": attr,
            "value": value
        })

    def edge_attr_changed(self, source_id, time_id, edge_id, attr, old_value, new_value):
        """An edge attribute was changed."""
        buff = bytearray()
        buff.extend(encoders.encode_byte(netstream.EVENT_CHG_EDGE_ATTR))
        buff.extend(source_id)
        buff.extend(encoders.encode_long(time_id))
        buff.extend(encoders.encode_string(edge_id))
        buff.extend(encoders.encode_string(attr))
        dtype = netstream.typeof(old_value)
        buff.extend(encoders.encode_byte(dtype))
        buff.extend(encoders.encode_value(old_value, dtype))
        dtype = netstream.typeof(new_value)
        buff.extend(encoders.encode_byte(dtype))
        buff.extend(encoders.encode_value(new_value, dtype))
        self.send_event(buff)
        logging.debug("edge attribute changed: %s", {
            "source_id": source_id,
            "time_id": time_id,
            "edge_id": edge_id,
            "attr": attr,
            "old_value": old_value,
            "new_value": new_value
        })

    def edge_attr_removed(self, source_id, time_id, edge_id, attr):
        """An edge attribute was removed."""
        buff = bytearray()
        buff.extend(encoders.encode_byte(netstream.EVENT_DEL_EDGE_ATTR))
        buff.extend(source_id)
        buff.extend(encoders.encode_long(time_id))
        buff.extend(encoders.encode_string(edge_id))
        buff.extend(encoders.encode_string(attr))
        self.send_event(buff)
        logging.debug("edge attribute removed: %s", {
            "source_id": source_id,
            "time_id": time_id,
            "edge_id": edge_id,
            "attr": attr
        })

class NetStreamProxyGraph(object):
    """Proxy object for sending graph events."""

    def __init__(self, sender, source_id=None):
        """Initialise using a sender and a source ID."""
        self.sender = sender
        self.source_id = None
        self.source_id_buff = None
        self.time_id = 0
        self.set_source_id(source_id)

    def set_source_id(self, source_id):
        """Set and cache the source ID for this graph proxy."""
        self.source_id = source_id if source_id \
            else "nss{}".format((long)(1000 * random.random()))
        self.source_id_buff = encoders.encode_string(self.source_id)

    def add_node(self, node):
        """Add a node to the graph."""
        self.sender.node_added(self.source_id_buff, self.time_id, node)
        self.time_id += 1

    def remove_node(self, node):
        """Remove a node from the graph."""
        self.sender.node_removed(self.source_id_buff, self.time_id, node)
        self.time_id += 1

    def add_edge(self, edge, from_node, to_node, directed=False):
        """Add an edge to the graph."""
        self.sender.edge_added(self.source_id_buff, self.time_id, edge, from_node, to_node, directed)
        self.time_id += 1

    def remove_edge(self, edge):
        """Remove an edge from the graph."""
        self.sender.edge_removed(self.source_id_buff, self.time_id, edge)
        self.time_id += 1

    def add_attribute(self, attr, value):
        """Add an attribute to the graph."""
        self.sender.graph_attr_added(self.source_id_buff, self.time_id, attr, value)
        self.time_id += 1

    def remove_attribute(self, attr):
        """Remove an attribute from the graph."""
        self.sender.graph_attr_removed(self.source_id_buff, self.time_id, attr)
        self.time_id += 1

    def change_attribute(self, attr, old_value, new_value):
        """Change an attribute of the graph."""
        self.sender.graph_attr_changed(self.source_id_buff, self.time_id, attr, old_value, new_value)
        self.time_id += 1

    def add_node_attribute(self, node, attr, value):
        """Add an attribute to a node."""
        self.sender.node_attr_added(self.source_id_buff, self.time_id, node, attr, value)
        self.time_id += 1

    def remove_node_attibute(self, node, attr):
        """Remove an attribute from a node."""
        self.sender.node_attr_removed(self.source_id_buff, self.time_id, node, attr)
        self.time_id += 1

    def change_node_attribute(self, node, attr, old_value, new_value):
        """Change an attribute of a node."""
        self.sender.node_attr_changed(self.source_id_buff, self.time_id, node, attr, old_value, new_value)
        self.time_id += 1

    def add_edge_attribute(self, edge, attr, value):
        """Add an attribute to an edge."""
        self.sender.edge_attr_added(self.source_id_buff, self.time_id, edge, attr, value)
        self.time_id += 1

    def remove_edge_attribute(self, edge, attr):
        """Remove an attribute from an edge."""
        self.sender.edge_attr_removed(self.source_id_buff, self.time_id, edge, attr)
        self.time_id += 1

    def change_edge_attribute(self, edge, attr, old_value, new_value):
        """Change an attribute of an edge."""
        self.sender.edge_attr_changed(self.source_id_buff, self.time_id, edge, attr, old_value, new_value)
        self.time_id += 1

    def clear_graph(self):
        """Clear the graph."""
        self.sender.graph_cleared(self.source_id_buff, self.time_id)
        self.time_id += 1

    def step_begins(self, time):
        """Begin a step."""
        self.sender.step_begun(self.source_id_buff, self.time_id, time)
        self.time_id += 1
