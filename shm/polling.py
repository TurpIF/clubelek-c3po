import time
import logging
from shm.server import build_client
from shm.exceptions import ConnectionFailed, ConnectionInterrupted

class Runner:
    SLEEP_TIME = 0.01

    def __init__(self):
        self.running = False
        # FIXME pass logger name
        self.logger = logging.getLogger(self.__class__.__name__)

    def start(self):
        """
        Setup and start the runner.
        """
        self.running = True
        self.logger.info('setting up')
        self.setup()
        self.logger.info('starting')
        self.run()

    def stop(self):
        """
        Stop the runner and cleanup.
        """
        self.logger.info('cleaning up')
        self.cleanup()
        self.running = False
        self.logger.info('stopping')

    def run(self):
        """
        Internal loop. Do not override unless you know what you are doing.
        """
        while self.running:
            try:
                self.step()
                time.sleep(self.SLEEP_TIME)
            except KeyboardInterrupt:
                self.logger.info('interrupted')
                self.stop()
            except Exception as e:
                self.logger.exception(e)
                raise

    def setup(self):
        """
        Runner initialization, called before run() is called.
        """
        pass

    def cleanup(self):
        """
        Runner cleanup, called after run() finishes.
        """
        pass

    def step(self):
        """
        Step function to implement in order to complete the runner logic.
        """
        raise NotImplementedError

class Poller(Runner):
    def __init__(self, property_descriptions, address, authkey):
        Runner.__init__(self)
        self.client = build_client(property_descriptions, address, authkey)
        self.property_descriptions = property_descriptions

    def setup(self):
        """
        Connect the client, remove properties that don't expose a getter method and reset the
        property cache to prepare polling.
        """
        try:
            self.client.connect()
        except IOError as e:
            raise ConnectionFailed('client cannot connect')
        self.properties = {name: getattr(self.client, name)()
                for name, _ in self.property_descriptions}
        self.property_cache = {}

    def step(self):
        """
        Poll all the properties for their values, calling property_changed()
        when one has changed.
        """
        for name, prop in self.properties.items():
            try:
                value = prop.get()
            except (IOError, EOFError) as e:
                raise ConnectionInterrupted('connection interrupted')
            else:
                cached_value = self.property_cache.get(name)
                if cached_value is None or cached_value != value:
                    self.property_cache[name] = value
                    self.property_changed(name, value)

    def property_changed(self, name, value):
        """
        Callback for when the value of a property changed.
        """
        pass
