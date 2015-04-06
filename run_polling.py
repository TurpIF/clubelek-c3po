"""
Poll data from a given bot.
"""
import argparse
import logging
from shm import Poller
from utils.scripting import server_address

logging.basicConfig(level=logging.INFO,
        format='[%(levelname)s][%(name)s][%(asctime)s] %(message)s')

class LoggingPoller(Poller):
    def property_changed(self, name, value):
        self.logger.info('%s=%s' % (name, value))

# script arguments
parser = argparse.ArgumentParser(description=__doc__)

parser.add_argument('address', type=server_address,
        help=('address of the server (can be an address in case of a UNIX '
              'socket or of the form address:port in case of a TCP socket'))
parser.add_argument('authkey', help='authentication key for the server')
parser.add_argument('--debug', action='store_true',
        help='set the logging level to debug')

if __name__ == '__main__':
    from bots.c3po import property_descriptions
    args = parser.parse_args()
    logger = logging.getLogger('SHM Poller(c3po)')
    if args.debug:
        logger.setLevel(logging.DEBUG)
    args.authkey = args.authkey.encode('ascii')

    poller = LoggingPoller(property_descriptions, args.address, args.authkey)
    logger.info('starting on %s' % (args.address,))
    poller.start()
