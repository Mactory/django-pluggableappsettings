import logging

__author__ = 'Tim Schneider <tim.schneider@northbridge-development.de>'
__copyright__ = "Copyright 2015, Northbridge Development Konrad & Schneider GbR"
__credits__ = ["Tim Schneider", ]
__maintainer__ = "Tim Schneider"
__email__ = "mail@northbridge-development.de"
__status__ = "Release"

logger = logging.getLogger(__name__)

class SettingsMetaClass(type):
    '''
    Metaclass that overwrides default class attribute access to load the functions on demand
    '''

    def __getattribute__(self, item):
        '''
        Function that is called whenever a class attribute is accessed.
        We then try to load the same setting from the django settings and use a default value as fallback if the
        setting does not exist

        :param item: The name of the attribute
        :return: The value of the attribute
        '''

        # Attributes that start with _DEFAULT_ are the default values and don't need to be looked up
        # Also if we already loaded the attribute previously, we don't need to look it up again
        if not item.startswith('_DEFAULT_') and not hasattr(self, item):

            # Load the value from settings but only if it is present
            from django.conf import settings
            if hasattr(settings, item):
                value = getattr(
                    settings,
                    item,
                    None,
                )
            else:
            # If the value is not present in the settings, we load the local _DEFAULT_<item> value
                default_name = '_DEFAULT_%s' % item
                # only load it if it exists
                if hasattr(self, default_name):
                    default = super(SettingsMetaClass, self).__getattribute__(default_name)
                    # call it if it is a callable
                    if hasattr(default, '__call__'):
                        value = default()
                    # or simply copy it
                    else:
                        value = default
                # if we don't have a default value, we raise an exception
                else:
                    raise AttributeError('Could not load Setting %s and has no default value defined' % item)

            # Add the value to the local class for future access
            setattr(self, item, value)
        # finally return the value
        return super(SettingsMetaClass, self).__getattribute__(item)


class AppSettings(object):
    '''
    Class that has the SettingsMetaClass ass metaclass. This is the base class for AppSettings classes
    '''
    __metaclass__ = SettingsMetaClass
