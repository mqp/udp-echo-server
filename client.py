#!/usr/bin/env python3
"""
A simple client for talking to a UDP echo server and logging the transactions.
"""
import argparse
import socket
import logging
import time

from helpers import receive_next

logger = logging.getLogger(__name__)
message = "Stuck in an AWS datacenter server closet, please send help.".encode()

def send_and_receive_one(sock, addr):
    "Sends a single datagram over the socket and waits for the response."
    output_len = sock.sendto(message, addr)
    logger.info("Sent %s bytes to %s.", output_len, addr)
    input_data, addr = receive_next(sock)
    logger.info("Received %s bytes back from %s.", len(input_data), addr)

def start(args):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1) # seconds
    try:
        while True:
            send_and_receive_one(sock, (args.host, args.port))
            time.sleep(1) # seconds
    finally:
        logger.info("Shutting down.")
        sock.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--host', help='The host that the client should connect to.', default="127.0.0.1")
    parser.add_argument('--port', help='The port that the client should connect to.', type=int, default=123)
    parser.add_argument('--verbose', '-v', help="Increases the logging verbosity level.", action='count')
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s')
    start(args)
