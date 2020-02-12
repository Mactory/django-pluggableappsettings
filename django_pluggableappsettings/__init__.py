import inspect
import logging
from pydoc import locate
import collections
from warnings import warn

__author__ = 'Tim Schneider <tim.schneider@northbridge-development.de>'
__copyright__ = "Copyright 2015 - 2016, Northbridge Development Konrad & Schneider GbR"
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

    def __init__(self, *args, **kwargs):
        super(SettingsMetaClass, self).__init__(*args, **kwargs)
        self._values = {}


    def __getattribute__(self, item_name):
        '''
        Function that is called whenever a class attribute is accessed.
        We then try to load the same setting from the django settings and use a default value as fallback if the
        setting does not exist

        :param item_name: The name of the attribute
        :return: The value of the attribute
        '''

        # first retrieve the item if possible
        try:
            item = super(SettingsMetaClass, self).__getattribute__(item_name)
        except AttributeError:
            raise AttributeError('The setting %s is not defined for this App' % item_name)

        if not isinstance(item, Setting):
            # we requested an item that is not a setting but still available, so we simply return it
            return item

        # we store all already loaded values in the _values dict, so we only have to load them once
        _values = super(SettingsMetaClass, self).__getattribute__('_values')

        # If it is not in _values, we need to load it
        if not item_name in _values:
            name_in_settings_py = item.get_settings_name() or item_name

            # load the value or one of its aliases from the settings or none if none exists
            from django.conf import settings
            settings_value = getattr(settings, name_in_settings_py, NOT_SET_VALUE)

            for alias in item.get_aliases():
                if settings_value != NOT_SET_VALUE:
                    break
                settings_value = getattr(settings, alias, NOT_SET_VALUE)

            # Pass the setting's value to the setting's class which can perform changes and then safe the value
            # so that it can be retrieved by the value() method
            item.get(item_name, settings_value)

            # Store the value in the dict so we only have to load it once
            _values[item_name] = item

        return _values[item_name].value()

class AppSettings(object, metaclass=SettingsMetaClass):
    """
    Class that has the SettingsMetaClass ass metaclass. This is the base class for AppSettings classes
    """
    pass


class Setting(object):
    """
    Baseclass for all settings types. Takes a default value as argument.
    Returns the settings value if it is not None or the default value instead.
    """
    _value = NOT_SET_VALUE

    def __init__(self, default_value=NOT_SET_VALUE, settings_name=None, aliases=[], ):
        """
        :param default_value: default value for this setting
        :param settings_name: Normally the user defined value for a setting is searched in the settings.py by the
        attribute name given to the settings instance. If the optional settings_name parameter is specified, this name
        is looked for instead (optional)
        :param aliases: Additional, optional, names which are looked for in the settings.py if the main setting name can
        not be found. (optional)
        :return:
        """
        self.default_value = default_value

        self._settings_name = settings_name

        # We only accept strings as aliases so
        # Use only strings from an iterable
        if isinstance(aliases, collections.Iterable):
            self._aliases = [a for a in aliases if isinstance(a, str)]
        # or ignore all aliases
        else:
            self._aliases = []

    def get_settings_name(self):
        return self._settings_name

    def get_aliases(self):
        """

        :return: The given aliases for this setting
        """
        return self._aliases

    def _get(self, setting_name, setting_value):
        """
        :param setting_name: the name of this setting. Needed for nice verbose output on errors
        :param setting_value: The value of the setting in settings.py. Pass None if the parameter is not set
        :return: setting_value if it is not None, else the default value. If that is also not set, an Attribute error
            is raised
        """
        if setting_value == NOT_SET_VALUE:
            if self.default_value == NOT_SET_VALUE:
                raise AttributeError(
                    'The setting %s is not defined in your settings.py and no default value is provided.' % (
                        self.get_settings_name() or setting_name
                    )
                )
            return self.default_value
        return setting_value

    def get(self, setting_name, setting_value):
        value = self._get(setting_name, setting_value)
        self._value = value

    def _get_value(self):
        if self._value == NOT_SET_VALUE:
            raise RuntimeError('Called value() method before the value was set by the get() method')
        return self._value

    def value(self):
        return self._get_value()

class CalledBaseSetting(Setting):
    """
    The setting which checks if the value is callable.
    """
    def __init__(self, *args, **kwargs):
        '''
        takes the 'force_callable' kwarg to set whether the value has to be callable
        :param args:
        :param kwargs:
        :return:
        '''
        self._force_callable = kwargs.pop('force_callable', False)
        super(CalledBaseSetting, self).__init__(*args, **kwargs)

    def _get(self, setting_name, setting_value):
        """
        uses the superclass to get the setting and verifies that the setting is callable
        :param setting_name: the name of this setting. Needed for nice verbose output on errors
        :param setting_value: The value of the setting in settings.py. Pass None if the parameter is not set
        :return: the settings value
        """
        val = super(CalledBaseSetting, self)._get(setting_name, setting_value)
        if self._force_callable and not hasattr(val, '__call__'):
            raise ValueError('The value for the setting %s has to be a callable.' % setting_name)
        return val

class CalledOnceSetting(CalledBaseSetting):
    """
    The setting calls it's callable value on first load.
    """
    def _get(self, setting_name, setting_value):
        """
        Returns the value or the return value of a call to value if the value has the '__call__' attribute
        :param setting_name: the name of this setting. Needed for nice verbose output on errors
        :param setting_value: The value of the setting in settings.py. Pass None if the parameter is not set
        :return: the value or the return value of a call to value if the value has the '__call__' attribute
        """
        val = super(CalledOnceSetting, self)._get(setting_name, setting_value)
        if hasattr(val, '__call__'):
            return val()
        return val


class CallableSetting(CalledOnceSetting):
    """
    The deprecated old Alias of a CalledOnceSetting.
    """
    def __init__(self, *args, **kwargs):
        warn('Deprecation Warning: The class CallableSetting has been renamed to CalledOnceSetting. This alias will be removed in a future version.')
        super(CallableSetting, self).__init__(*args, **kwargs)


class CalledEachTimeSetting(CalledBaseSetting):
    """
    The setting which calles the callable value each time the setting's value is requested.
    """
    def _get_value(self):
        """
        Returns the value or the return value of a call to value if the value has the '__call__' attribute
        """
        val = super(CalledEachTimeSetting, self)._get_value()
        if hasattr(val, '__call__'):
            return val()
        return val


class ClassSetting(Setting):
    """
    A Setting which expects a class or a dotted path to a class
    """
    def _get(self, setting_name, setting_value):
        """
        :param setting_name: the name of this setting. Needed for nice verbose output on errors
        :param setting_value: The value of the setting in settings.py.
        :return: the settings_value or the default value. This is guaranteed to be a class type
        :except: ValueError if the setting_value (or the fallback) is not a class and not dotted string to a class
        """
        val = super(ClassSetting, self)._get(setting_name, setting_value)
        if not inspect.isclass(val):
            if not isinstance(val, str):
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

    def _get(self, setting_name, setting_value):
        """
        :param setting_name: the name of this setting. Needed for nice verbose output on errors
        :param setting_value: The value of the setting in settings.py.
        :return: the settings_value or the default value. This is guaranteed to be a class type
        :except: ValueError if the setting_value (or the fallback) is not of the provided type
        """
        if self._setting_type is None:
            raise AttributeError('The _setting_type attribute of type %(type)s needs to be set for the check to work' % {'type': self.__class__.__name__})
        val = super(TypedSetting, self)._get(setting_name, setting_value)
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
    _setting_type = str
    _cast_value = False

class IterableSetting(TypedSetting):
    """
    An iterable setting
    """
    _setting_type = collections.Iterable
    _cast_value = False