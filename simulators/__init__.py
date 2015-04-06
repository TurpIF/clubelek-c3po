class BaseSimulator:
    """
    Base simulator class.

    Simulators are implemented through update() method which take a shm client
    and apply a transformation depending on the current state.
    """
    rate = 1 / 30

    def update(self, client):
        raise NotImplementedError


class PIDController:
    """
    Generic PID computation controller.
    """
    def __init__(self, kp, ki, kd, integrator_min, integrator_max, derivator=0, integrator=0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.derivator = derivator
        self.integrator = integrator
        self.integrator_max = integrator_max
        self.integrator_min = integrator_min
        self.order = 0.0

    def update(self, current_value):
        """
        Calculate PID output value for given reference input and feedback.
        """
        error = self.order - current_value

        p_value = self.kp * error
        d_value = self.kd * (error - self.derivator)
        self.derivator = error

        self.integrator = self.integrator + error

        if self.integrator > self.integrator_max:
                self.integrator = self.integrator_max
        elif self.integrator < self.integrator_min:
                self.integrator = self.integrator_min

        i_value = self.integrator * self.ki

        return p_value + i_value + d_value

    def set_order(self, order, derivator=0, integrator=0):
        """
        Initilize the setpoint of PID
        """
        self.order = order
        self.derivator = derivator
        self.integrator = integrator


class Trapezium:
    def __init__(self, max_vel, max_acc, value=0, velocity=0):
        self.max_vel = max_vel
        self.max_acc = max_acc
        self.value = value
        self.velocity = velocity

    def update(self, new_value):
        dv = new_value - self.value
        if dv >= self.max_vel:
            dv = self.max_vel
        elif dv <= -self.max_vel:
            dv = -self.max_vel

        da = dv - self.velocity
        if da >= self.max_acc:
            da = self.max_acc
        elif da <= -self.max_acc:
            da = -self.max_acc

        self.velocity += da
        self.value += self.velocity


# simulators available
from simulators.translation import Translation
from simulators.linear import LinearSimulator

def simulator_factory(prop_name, *args, **kwargs):
    prop_getter = lambda c: getattr(c, prop_name)()
    order_getter = lambda c: getattr(c, prop_name + '_order')()
    return lambda: LinearSimulator(prop_getter, order_getter)(*args, **kwargs)

_available_simulators = {
        'translation': lambda: Translation(),
        'left_arm': simulator_factory('left_arm', 1.0, 0.2, 0.5, 0, 0.2)
        }

class NoSuchSimulator(ValueError):
    pass

def get_simulator(name):
    """
    Return the simulator asked for, if available (otherwise raises
    NoSuchSimulator).
    """
    try:
        return _available_simulators[name]
    except KeyError:
        raise NoSuchSimulator


def available_simulators():
    """Return a list of available simulators."""
    return list(_available_simulators.keys())
