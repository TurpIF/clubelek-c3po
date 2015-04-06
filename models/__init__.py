import logging
from time import time

logging.basicConfig(level=logging.INFO,
        format='[%(levelname)s][%(name)s][%(asctime)s] %(message)s')

class Game:
    def __init__(self, bot, world, time_max=90.0):
        '''
        Construct a empty game with a map and a maximum time.
        Time is in seconds.

        bot: bot.Base
        world: World
        time_max: float (sec)
        '''
        self.logger = logging.getLogger('Game')

        self.time_max = time_max
        self.begin_epoch = None
        self.world = world
        self.bot = bot

    def start(self):
        '''
        Start the game
        '''
        if self.begin_epoch is None:
            self.begin_epoch = time()
            self.logger.info('Start of the game')
        else:
            self.logger.warning('Already started')

    @property
    def time(self):
        '''
        Return the elapsed time during the beginning of the game
        '''
        if self.begin_epoch is None:
            return None
        return time() - self.begin_epoch


class BaseWorld:
    '''
    World of the game with allies, ennemies and items
    '''

    def __init__(self, allies=list(), ennemies=list(), items=list()):
        '''
        allies: list(bot.Base)
        ennemies: list(bot.Base)
        items: list(BaseItem)
        '''
        self.allies = allies
        self.ennemies = ennemies
        self.items = items


class BaseItem:
    '''
    Item of the game on the map.
    This class could be inherited to add a state to the item (for example
    open/close for the claps in 2014-2015).
    Each item is identified with an unique ID  and has a item type.
    '''

    uid = 42

    def __init__(self, _type, position, radius):
        '''
        _type: string or enum or whatever (it's your job)
        position: (float (mm), float (mm))
        radius: float (mm)
        '''
        self.uid = AbstractItem.uid
        AbstractItem += 1
        self._type = _type
        self.position = position
        self.radius = radius


class Task:
    '''
    Represent a task to do for a bot.
    It's modelized with two main bot states : pre-condition, post-condition.
    The pre-condition is the state of the bot required before doing the task.
    The post-condition indicates the state after the task.
    A cancel state could be given in order to manage the case of the task is
    canceled (or aborded)
    '''

    def __init__(self, precond=None, postcond=None, cancel=None):
        '''
        precond: bot.BaseState
        postcond: bot.BaseState
        cancel: bot.BaseState
        '''
        self.precondition = precond
        self.postcondition = postcondition
        self.cancel = cancel

    def realizable(self, bot):
        '''
        Return if the bot can realize this task
        This should be checked before trying to do the task

        bot: bot.Base
        '''
        raise NotImplementedError
