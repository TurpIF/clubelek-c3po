import argparse
from shm import build_client
from utils.scripting import server_address

parser = argparse.ArgumentParser(description=__doc__)

parser.add_argument('address', type=server_address,
        help=('address of the server (can be an address in case of a UNIX '
              'socket or of the form address:port in case of a TCP socket'))
parser.add_argument('authkey', help='authentication key for the server')

if __name__ == '__main__':
    args = parser.parse_args()
    print(args)
