from multiprocessing import Lock
from functools import partial as _bind

class BaseProperty:
    """
    Base interface for properties, who always should extend this class.
    """
    def __init__(self):
        """Initialize the property with a multiprocess lock."""
        self.lock = Lock()

    # list of exposed methods through the shm
    EXPOSED = ('typeid', 'get', 'set')

    def typeid(self):
        """Retreive a unique identifier for the property's type."""
        return self.__class__.__name__

    def get(self):
        """
        Return the data representation of this property.
        """
        with self.lock:
            return self.get_value()

    def set(self, value):
        """
        Change the data for this property, the value should be unpacked here,
        raising by convention a ValueError if the value given won't fit for
        this property, or a TypeError if the datatype isn't valid.
        """
        with self.lock:
            self.set_value(value)

    def get_value(self):
        """Implement this method with the property's actual getting method."""
        raise NotImplementedError

    def set_value(self, value):
        """Implement this method with the property's actual setting method."""
        raise NotImplementedError

class Value(BaseProperty):
    """
    The most simple property, a simple single value. The given value must be
    JSON serializable.

    TODO type/value checking?
    """
    def __init__(self, value):
        BaseProperty.__init__(self)
        self.value = self.format_value(value)

    def format_value(self, value):
        """
        Called right before setting the value, formats the value and can raise
        TypeError / ValueError in case the value isn't correct.
        """
        return value

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = self.format_value(value)

class TypedValue(Value):
    """Value with a type."""
    def __init__(self, value, type):
        self.type = type
        Value.__init__(self, value)

    def format_value(self, value):
        return self.type(value)

class Array(Value):
    def __init__(self, value, type=None, length=None):
        self.type = type
        self.length = length
        Value.__init__(self, value)

    def format_value(self, value):
        if self.length is not None and self.length != len(value):
            raise ValueError('array should be of length %s' % self.length)
        if self.type is not None:
            value = tuple((self.type(v) for v in value))
        return Value.format_value(self, value)

# basic types
class Bool(TypedValue):
    def __init__(self, value):
        TypedValue.__init__(self, value, type=bool)

class Int(TypedValue):
    def __init__(self, value):
        TypedValue.__init__(self, value, type=int)

class Float(TypedValue):
    def __init__(self, value):
        TypedValue.__init__(self, value, type=float)

# composite but basic types
class Point(Array):
    def __init__(self, x, y, z):
        Array.__init__(self, (x, y, z), type=float, length=3)
