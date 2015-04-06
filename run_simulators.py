"""
Run a number of simulators on a running shm manager.
"""
import os
import time
import logging
import argparse
from shm import build_client
from utils.scripting import server_address, positive_int
from simulators import BaseSimulator, get_simulator

logging.basicConfig(level=logging.INFO,
        format='[%(levelname)s][%(name)s][%(asctime)s] %(message)s')

parser = argparse.ArgumentParser(description=__doc__)

def simulator_name(name):
    """
    Argparse type taking a simulator name.
    """
    try:
        return get_simulator(name)
    except ImportError as e:
        raise argparse.ArgumentError('invalid simulator %s' % name) from e

parser.add_argument('address', type=server_address,
        help=('address of the server (can be an address in case of a UNIX '
              'socket or of the form address:port in case of a TCP socket'))
parser.add_argument('authkey', help='authentication key for the server')
parser.add_argument('simulators', type=simulator_name, nargs='+',
        help='simulators to run')
parser.add_argument('-r', '--rate', type=positive_int, default=30,
        help='update rate of the simulators (~FPS)')

if __name__ == '__main__':
    from bots.c3po import property_descriptions
    args = parser.parse_args()
    args.authkey = args.authkey.encode('ascii')

    # setup logging
    logger = logging.getLogger('C3PO Simulator(c3po)')

    # connect client
    client = build_client(property_descriptions, args.address, args.authkey)
    logger.info('connecting to shm server on %s' % args.address)
    client.connect()

    # initialize simulators
    simulators = []
    for simulator_cls in args.simulators:
        simulator = simulator_cls()
        simulator.rate = args.rate # hint the simulator rate
        simulators.append(simulator)

    # run simulators
    try:
        while True:
            logger.info('running simulators')
            for simulator in simulators:
                logger.info('running simulator %s' % simulator.__class__.__name__)
                simulator.update(client)
            time.sleep(1 / args.rate)
    except KeyboardInterrupt:
        logger.info('interrupted')
