import os
import sys
import time
import logging
import argparse
import threading
from flask import Flask, request, abort, jsonify
from utils.scripting import server_address, positive_int
from utils.strings import slugify
import shm
from simulators import get_simulator, available_simulators, NoSuchSimulator

logging.basicConfig(level=logging.INFO,
       format='[%(levelname)s][%(name)s][%(asctime)s] %(message)s')

this_dir = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__, static_url_path='',
            static_folder=os.path.join(this_dir, 'webview', 'static'))

@app.route('/')
def home():
    """Return the app index."""
    return app.send_static_file('index.html')

def api_route(path, *args, **kwargs):
    """
    Decorator encapsulating `app.route` for api endpoints, simply adding the
    /api prefix.
    """
    if not path.startswith('/'):
        path = '/%s' % path
    return app.route('/api%s' % path, *args, **kwargs)

def api_error(message, status_code):
    """Return an API error given a message and a status code."""
    response = jsonify({'error': message})
    response.status_code = status_code
    return response

@app.before_request
def check_api_requirements():
    """
    Before each api request using the <bot_id> argument, check that it is
    valid, otherwise returning a 400 (bad request).

    TODO: check that the bot's SHM server is available?
    """
    if not request.path.startswith('/api'):
        return
    if request.view_args is None or 'bot_id' not in request.view_args:
        return
    if request.view_args['bot_id'] not in app.config['BOTS']:
        abort(400)


@app.errorhandler(shm.ConnectionError)
def api_shm_error(err):
    return api_error('connection to shm server failed', 504)


def bot_properties(bot_id):
    """
    Return all available properties for the given bot. The bot id should be
    available in the `app.config` dictionary.
    """
    bot_config = app.config['BOTS'][bot_id]
    return [pd[0] for pd in bot_config['properties']]


def build_bot_client(bot_id):
    """
    Wrapper building a shm client given a bot id. The bot id should be
    available in the `app.config` dictionary.
    """
    bot_config = app.config['BOTS'][bot_id]
    client = shm.build_client(bot_config['properties'],
                              bot_config['address'], bot_config['authkey'])

    # connect or through a ConnectionError
    try:
        client.connect()
    except IOError as e:
        raise shm.ConnectionError
    return client


@api_route('/bots', methods=['GET'])
def bots():
    """
    Retreive the registered bots as a mapping from bot id to bot data (for the
    moment, only the address).
    """
    return jsonify({
        'bots': [{'id': bot_id, 'address': bot_data['address']}
                 for bot_id, bot_data in app.config['BOTS'].items()]
        })


def list_properties(bot_id):
    """
    List the properties for the given bot, returning a list of properties, each
    one of them a dict with the following data:
    - name: the name of the property
    - value: the value of the property
    - type: the type of the property
    """
    client = build_bot_client(bot_id)
    props = []
    for name in bot_properties(bot_id):
        prop = getattr(client, name)()
        props.append({
            'name': name,
            'type': slugify(prop.typeid()),
            'value': prop.get()
            })
    return props


def update_property(bot_id, name, value):
    """
    Update a property for a given bot and property name/value. Throws a few
    exceptions in case the update process fails:
    - AttributeError: unknown property
    - TypeError, ValueError: invalid value

    Returns the real value set.
    """
    client = build_bot_client(bot_id)
    prop = getattr(client, name)()
    prop.set(value)
    return value


@api_route('/<bot_id>/properties', methods=['GET', 'PATCH'])
def properties(bot_id):
    """
    In the case of a GET request, pull out the properties as a JSON dictionary
    (mapping property name to value), set for key 'properties'. In the case of
    a PATCH request, update the given properties with the new values.
    """
    if request.method == 'GET':
        properties = list_properties(bot_id)
        return jsonify({'properties': properties})
    else:
        # get request parameters (name and value)
        parameters = request.json
        try:
            data = parameters['properties']
            name, value = data['name'], data['value']
        except (TypeError, KeyError) as e:
            app.logger.exception(e)
            return api_error('bad request parameters', 400)

        # update property
        try:
            value = update_property(bot_id, name, value)
            return jsonify({'property': { 'name': name, 'value': value }})
        except (ValueError, TypeError) as e:
            return api_error('invalid value', 400)
        except AttributeError as e:
            return api_error('unknown property', 404)
        except shm.ConnectionError as e:
            return api_error('connection failed: %s' % e, 502)


class SimulatorThread(threading.Thread):
    """
    Simulator thread, handling all simulator setup and simulation logic.

    The thread can be requested to stop by setting the `evt` threading.Event
    (via the set() method). It can be joined afterwards to guarantee proper
    cleanup.
    """
    def __init__(self, bot_id, name, rate=None):
        threading.Thread.__init__(self)

        # event used to stop the simulator thread
        self.evt = threading.Event()

        # load up the simulator
        try:
            simulator_cls = get_simulator(name)
        except NoSuchSimulator as e:
            app.logger.exception(e)
        else:
            self.simulator = simulator_cls()

        # override the rate if it was given
        if rate is None:
            rate = app.config['SIMULATORS']['rate']
        self.simulator.rate = rate
        self.bot_id = bot_id

    def run(self):
        try:
            client = build_bot_client(self.bot_id)
            while not self.evt.is_set():
                self.simulator.update(client)
                time.sleep(1.0 / self.simulator.rate)
        except shm.ConnectionError as e:
            app.logger.exception(e)


# information on running simulators
running_simulators_lock = threading.Lock()
running_simulators = {}


@api_route('/<bot_id>/simulators/<name>', methods=['POST', 'DELETE'])
def manage_simulators(bot_id, name):
    """
    Control the requested simulator of a bot by either starting (POST) or
    stopping it (DELETE). No fields are required in the request.
    """
    running_simulators.setdefault(bot_id, {})

    # check that the given simulator is valid
    if name not in available_simulators():
        return api_error('unknown simulator', 404)

    if request.method == 'POST':
        if name in running_simulators[bot_id]:
            return api_error('simulator already running', 412)

        # start a simulator thread
        simulator_t = SimulatorThread(bot_id, name)
        simulator_t.start()

        # update the running simulator memory
        with running_simulators_lock:
            running_simulators[bot_id][name] = simulator_t
    else:
        if name not in running_simulators[bot_id]:
            return api_error('simulator not running', 412)

        # stop the simulator thread
        with running_simulators_lock:
            simulator_t = running_simulators[bot_id][name]
            simulator_t.evt.set()
            simulator_t.join()

        # update the running simulator memory
        with running_simulators_lock:
            del running_simulators[bot_id][name]

    return jsonify({'simulator': name})


@api_route('/<bot_id>/simulators', methods=['GET'])
def list_simulators(bot_id):
    """
    List the available simulators for a bot.
    """
    running_simulators.setdefault(bot_id, {})
    return jsonify({'simulators': {name: name in running_simulators[bot_id]
                                   for name in available_simulators()}})


@api_route('/<bot_id>/ai', methods=['POST', 'DELETE'])
def ai(bot_id):
    """
    Control the AI of a bot by either starting (POST) or stopping it (DELETE).
    No fields are required in the request.
    """
    abort(501) # TODO


# script arguments
parser = argparse.ArgumentParser(description=__doc__)

parser.add_argument('address', type=server_address,
        help=('address of the server (can be an address in case of a UNIX '
              'socket or of the form address:port in case of a TCP socket'))
parser.add_argument('authkey', help='authentication key for the server')
parser.add_argument('--debug', action='store_true',
        help='start the app in debug mode')
parser.add_argument('-r', '--rate', type=positive_int, default=30,
        help='update rate of the simulators (~FPS)')

if __name__ == '__main__':
    from rules.bots.c3po import property_descriptions
    args = parser.parse_args()
    args.authkey = args.authkey.encode('ascii')

    app.config['SIMULATORS'] = {
            'rate': args.rate
        }
    app.config['BOTS'] = {
            'c3po': {
                'address': args.address,
                'authkey': args.authkey,
                'properties': property_descriptions
                }
            }

    app.run(debug=args.debug)

    # stop simulator threads
    with running_simulators_lock:
        if running_simulators:
            app.logger.info('stopping simulators')
        for simulators in running_simulators.values():
            for simulator_t in simulators.values():
                simulator_t.evt.set()
        for simulators in running_simulators.values():
            for simulator_t in simulators.values():
                simulator_t.join()
