#!/usr/bin/env python3
"""
A simple client for talking to a UDP echo server and logging the transactions.
"""
import argparse
import itertools
import logging
import socket
import time

logger = logging.getLogger(__name__)

# the buffer for receiving incoming messages
BUFFER_SIZE = 4096

def send_and_receive_one(sock, message, addr):
    "Sends a single datagram over the socket and waits for the response."
    output_len = sock.sendto(message.encode(), addr)
    logger.info("Sent message to %s: %s (%s bytes).", addr, message, output_len)
    try:
        input_data, addr = sock.recvfrom(BUFFER_SIZE)
        logger.info("Received message back from %s: %s (%s bytes).", addr, input_data.decode(), len(input_data))
    except socket.timeout:
        logger.warning("Message never received back from %s: (%s).", addr, message)

def start(args):
    "Starts sending messages to the server."
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1) # seconds
    addr = (args.host, args.port)
    try:
        for i in itertools.count(1):
            message = "This is message #{}.".format(i)
            send_and_receive_one(sock, message, addr)
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
