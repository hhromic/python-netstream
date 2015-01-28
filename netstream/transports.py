"""Transport implementations for the NetStream protocol."""

import socket
import logging

class BinaryNetStreamTransport(object):
    """Default transport class using raw binary data."""
    def __init__(self, host, port):
        """Initialise using host and port."""
        self.host = host
        self.port = port
        self.socket = None

    def connect(self):
        """Connect to remote server if necessary."""
        if self.socket:
            logging.debug("already connected")
            return True
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            logging.info("connected to remote server")
            return True
        except socket.error as err:
            self.socket = None
            logging.error(err)
            return False

    def send(self, data):
        """Send raw binary data to remote server."""
        if not self.socket:
            if not self.connect():
                return False
        try:
            self.socket.sendall(data)
            return True
        except socket.error as err:
            self.socket = None
            logging.error(err)
            return False

    def close(self):
        """Close the connection."""
        if self.socket:
            self.socket.close()
            self.socket = None
            logging.info("disconnected from remote server")
