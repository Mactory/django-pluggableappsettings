import inspect
import logging
from pydoc import locate
import collections

__author__ = 'Tim Schneider <tim.schneider@northbridge-development.de>'
__copyright__ = "Copyright 2015, Northbridge Development Konrad & Schneider GbR"
__credits__ = ["Tim Schneider", ]
__maintainer__ = "Tim Schneider"
__email__ = "mail@northbridge-development.de"
__status__ = "Release"

logger = logging.getLogger(__name__)

NOT_SET_VALUE = object()

class SettingsMetaClass(type):
    '''
    Metaclass that overwrites default class attribute access to load the functions on demand
    '''

    def __getattribute__(self, item):
        '''
        Function that is called whenever a class attribute is accessed.
        We then try to load the same setting from the django settings and use a default value as fallback if the
        setting does not exist

        :param item: The name of the attribute
        :return: The value of the attribute
        '''

        # we store all already loaded values in the _values dict, so we only have to load them once
        _values = super(SettingsMetaClass, self).__getattribute__('_values')

        # If it is not in _values, we need to load it
        if not item in _values:
            # first see, if it is defined at all
            try:
                setting = super(SettingsMetaClass, self).__getattribute__(item)
            except AttributeError:
                raise AttributeError('The setting %s is not defined for this App' % item)

            # then load the values from the settings or none if it does not exist
            from django.conf import settings
            settings_value = getattr(settings, item, NOT_SET_VALUE)

            # Use the setting's class to handle the settings value or return the default value
            value = setting.get(item, settings_value)

            # Store the value in the dict so we only have to load it once
            _values[item] = value

        return _values[item]


class AppSettings(object):
    """
    Class that has the SettingsMetaClass ass metaclass. This is the base class for AppSettings classes
    """
    __metaclass__ = SettingsMetaClass
    _values = {}


class Setting(object):
    """
    Baseclass for all settings types. Takes a default value as argument.
    Returns the settings value if it is not None or the default value instead.
    """
    def __init__(self, default_value=NOT_SET_VALUE):
        """
        :param default_value: default value for this setting
        :return:
        """
        self.default_value = default_value

    def get(self, setting_name, setting_value):
        """
        :param setting_name: the name of this setting. Needed for nice verbose output on errors
        :param setting_value: The value of the setting in settings.py. Pass None if the parameter is not set
        :return: setting_value if it is not None, else the default value. If that is also not set, an Attribute error
            is raised
        """
        if setting_value == NOT_SET_VALUE:
            if self.default_value == NOT_SET_VALUE:
                raise AttributeError(
                    'The setting %s is not defined in your settings.py and no default value is provided.' % setting_name
                )
            return self.default_value
        return setting_value


class CallableSetting(Setting):
    """
    The setting which also checks if the setting_value can be called, and does so if possible.
    """
    def get(self, setting_name, setting_value):
        """
        uses the superclass to get the setting and then calls it if possible
        :param setting_name: the name of this setting. Needed for nice verbose output on errors
        :param setting_value: The value of the setting in settings.py. Pass None if the parameter is not set
        :return: setting_value if it is not None, else the default value. If that is also not set, an Attribute error
            is raised. If the returned value can be called, it is called before returning
        """
        val = super(CallableSetting, self).get(setting_name, setting_value)
        if hasattr(val, '__call__'):
            val = val()
        return val

class ClassSetting(Setting):
    """
    A Setting which expects a class or a dotted path to a class
    """
    def get(self, setting_name, setting_value):
        """
        :param setting_name: the name of this setting. Needed for nice verbose output on errors
        :param setting_value: The value of the setting in settings.py.
        :return: the settings_value or the default value. This is guaranteed to be a class type
        :except: ValueError if the setting_value (or the fallback) is not a class and not dotted string to a class
        """
        val = super(ClassSetting, self).get(setting_name, setting_value)
        if not inspect.isclass(val):
            if not isinstance(val, basestring):
                raise ValueError('The value for the setting %s either has to be a class or a string containing the dotted path of a class.' % setting_name)
            val_string = val
            val = locate(val_string)
            if val is None:
                raise ValueError('The class described by "%s" for the setting %s could not be found.' % (val_string, setting_name))
        return val

class TypedSetting(Setting):
    """
    A Setting that checks the value to be of a certain type
    """
    _setting_type = None
    _cast_value = False

    def cast_value(self, value):
        """
        :param value: the current settings value
        :return: The casted value if _cast_value is set to true. Otherwise the value itself
        """
        return self._setting_type(value) if self._cast_value else value

    def get(self, setting_name, setting_value):
        """
        :param setting_name: the name of this setting. Needed for nice verbose output on errors
        :param setting_value: The value of the setting in settings.py.
        :return: the settings_value or the default value. This is guaranteed to be a class type
        :except: ValueError if the setting_value (or the fallback) is not of the provided type
        """
        if self._setting_type is None:
            raise AttributeError('The _setting_type attribute of type %(type)s needs to be set for the check to work' % {'type': self.__class__.__name__})
        val = super(TypedSetting, self).get(setting_name, setting_value)
        try:
            val = self.cast_value(val)
        except:
            raise ValueError('The value for setting %(setting)s cannot be casted to type %(type)s' % {'setting': setting_name, 'type': self._setting_type.__name__})
        if not isinstance(val, self._setting_type):
            raise ValueError('The value for setting %(setting)s is not of type %(type)s' % {'setting': setting_name, 'type': self._setting_type.__name__})
        return val

class IntSetting(TypedSetting):
    """
    An integer setting
    """
    _setting_type = int
    _cast_value = True

class FloatSetting(TypedSetting):
    """
    A float setting
    """
    _setting_type = float
    _cast_value = True

class StringSetting(TypedSetting):
    """
    A string setting
    """
    _setting_type = basestring
    _cast_value = False

class IterableSetting(TypedSetting):
    """
    An iterable setting
    """
    _setting_type = collections.Iterable
    _cast_value = False