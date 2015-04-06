import argparse
from shm import parse_server_address

def server_address(path):
    """
    Argparse type taking a shm server address spec.
    """
    try:
        return parse_server_address(path)
    except BadConnectionIdentifier as e:
        raise argparse.ArgumentError('server port should be an integer')

def positive_int(nb):
    """
    Argparse type taking a positive integer.
    """
    try:
        nb = int(nb)
    except ValueError as e:
        raise argparse.ArgumentError('excepted an integer, got %s' % nb)
    if nb <= 0:
        raise argparse.ArgumentError('excepted a positive integer, got %s' % nb)
