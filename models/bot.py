class Base:
    '''
    Base bot
    All static properties has to be defined here (in subclasses).
    All dynamic properties has to be in put in *real_state* (and *order_state*)
    which are *BaseState* instances.
    '''

    def __init__(self, name, radius, real_state=None, order_state=None, tasks=list()):
        '''
        name: string
        radius: float (mm)
        real_state: BaseState
        order_state: BaseState
        tasks: list(AbstractTask)
        '''
        self.name = name
        self.radius = radius
        self.tasks = tasks
        self.real_state = real_state
        self.order_state = order_state


class BaseState:
    '''
    Basic dynamic state of a bot.
    Should be inherited to add other dynamic properties.
    '''

    def __init__(self, position=None, velocity=None, acceleration=None,
            items=list()):
        '''
        position: tuple(float (mm), float (mm), float (radian))
        velocity: tuple(float (mm), float (mm), float (radian))
        acceleration: tuple(float (mm), float (mm), float (radian))
        items: list(BaseItem)
        '''
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.items = items


class Enemy:
    '''
    Represent informations about ennemies.
    *state* should be an instance of BaseState. It could be an instance of a
    subclass if more properties could be use.
    '''

    def __init__(self, name, radius, state=None):
        '''
        name: string
        radius: float (mm)
        state: BaseState
        '''
        self.name = name
        self.radius = radius
        self.state = state
