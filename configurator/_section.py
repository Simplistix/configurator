# Copyright (c) 2011-2012 Simplistix Ltd
# See license.txt for license details.

from . import marker
from ._api import API
from ._utils import get_source

class Section(object):
    """
    This is the class used to store configuration information.
    It provides mapping and attribute access to configuration
    values and can also contain sub-sections by way of nested
    :class:`Section` instances.
    """

    def __init__(self, source=None):
        """
        Create a new configuration section.
        
        The source location that this section came from can also be supplied as
        a string. While this is optional, it is strongly recommended.
        """
        self._api = API(source or get_source())

    def __getitem__(self, name):
        """
        Access a configuration value by name. If no configuration item exists
        for that name, a :class:`KeyError` will be raised.
        """
        value =  self._api.get(name, marker)
        if value is marker:
            raise KeyError(name)
        return value
    
    def __setitem__(self, name, value):
        """
        Set a value for a name in this section.
        If possible, the :func:`~configurator.api` for a section should be used
        to set configuration values.
        """
        self._api.set(name, value, source=get_source())

    def get(self, name, default=None):
        """
        Return the value associated with the supplied name in this
        :class:`Section`. If no value is associated, the supplied default is
        returned. If no default is supplied, ``None`` will be returned.
        """
        return self._api.get(name, default)
    
    def __getattr__(self, name):
        """
        Access a configuration value by name. If no configuration item exists
        for that name, an :class:`AttributeError` will be raised.
        """
        value = self._api.get(name, marker)
        if value is marker:
            raise AttributeError(name)
        return value

    def __setattr__(self, name, value):
        """
        Set a value for a name in this section.
        If possible, the :func:`~configurator.api` for a section should be used
        to set configuration values.
        """
        if name == '_api':
            self.__dict__[name] = value
        else:
            self._api.set(name, value, get_source())

    def keys(self):
        """
        A generator that yields the names available in this section.
        Un-named values will not be returned.
        """
        for a in self._api.items():
            if a.name:
                yield a.name

    def values(self):
        """
        A generator that yields the values stored in this section.
        Un-named values will be returned.
        """
        for a in self._api.items():
            yield a.value

    def items(self):
        """
        A generator that yields the ``(name, value)`` tuples for the
        information stored in this section.
        Un-named values will be returned and the `name` in the tuple will
        be ``None``.
        """
        for a in self._api.items():
            yield a.name, a.value

    def __iter__(self):
        "This will return the :meth:`items` generator."
        return self.keys()