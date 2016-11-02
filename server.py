#!/usr/bin/env python3
"""
A simple UDP echo server.
"""
import argparse
import socket
import logging

from helpers import receive_next

logger = logging.getLogger(__name__)

def receive_and_send_one(sock):
    "Waits for a single datagram over the socket and echoes it back."
    input_data, addr = receive_next(sock)
    logger.info("Received %s bytes from %s.", len(input_data), addr)
    output_len = sock.sendto(input_data, addr)
    logger.info("Echoed %s bytes back to %s.", output_len, addr)

def start(args):
    "Runs the server."
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1) # seconds
    sock.bind((args.host, args.port))
    logger.info("Listening on %s:%s.", args.host, args.port)
    try:
        while True:
            receive_and_send_one(sock)
    finally:
        logger.info("Shutting down.")
        sock.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--host', help='The host that the server socket should bind to.', default="0.0.0.0")
    parser.add_argument('--port', help='The port that the server socket should bind to.', type=int, default=123)
    parser.add_argument('--verbose', '-v', help="Increases the logging verbosity level.", action='count')
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    start(args)
