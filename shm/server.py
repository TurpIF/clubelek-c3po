from multiprocessing.managers import BaseManager
from shm.properties import BaseProperty

def build_client(properties, address, authkey):
    """
    Build a shared memory manager client.
    """
    class Manager(BaseManager):
        pass

    if not properties:
        properties = list()

    for name, _ in properties:
        Manager.register(name)

    manager = Manager(address=address, authkey=authkey)
    return manager

def build_server(properties, address, authkey):
    """
    Build a shared memory manager server.
    """
    class Manager(BaseManager):
        pass

    if not properties:
        properties = list()

    for name, getter in properties:
        Manager.register(name, getter, exposed=BaseProperty.EXPOSED)

    manager = Manager(address=address, authkey=authkey)
    return manager.get_server()

def parse_server_address(path):
    """
    Parse an address spec, taking either a UNIX socket or a ADDRESS:PORT spec
    for the shm manager's server address.
    Raises a BadConnectionIdentifier if the spec doesn't match.
    """
    # check if it's a address:port spec
    address_tuple = path.split(':')
    if len(address_tuple) == 2:
        address, port = address_tuple
        try:
            return address, int(port)
        except ValueError as e:
            raise BadConnectionIdentifier('bad address spec "%s"' % path)
    return path
