"""
Helpers for working with sockets.
"""
import socket
import logging

logger = logging.getLogger(__name__)

# the buffer for receiving incoming messages
BUFFER_SIZE = 4096

def receive_next(sock):
    "Repeatedly tries receiving on the given socket until some data comes in."
    logger.debug("Waiting to receive data...")
    while True:
        try:
            return sock.recvfrom(BUFFER_SIZE)
        except socket.timeout:
            logger.debug("No data received yet: retrying.")
            pass
