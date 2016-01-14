# -*- coding: utf-8 -*-
from __future__ import absolute_import
import logging

from django.test.utils import override_settings

from django_pluggableappsettings import Setting

__author__ = 'Tim Schneider <tim.schneider@northbridge-development.de>'
__copyright__ = "Copyright 2016, Northbridge Development Konrad & Schneider GbR"
__credits__ = ["Tim Schneider", ]
__maintainer__ = "Tim Schneider"
__email__ = "mail@northbridge-development.de"
__status__ = "Development"

logger = logging.getLogger(__name__)

class MockSetting(Setting):
    def __init__(self, value):
        '''
        Enforce the usage of a value
        :param value:
        :return:
        '''
        super(MockSetting, self).__init__(value)

    def _get_value(self):
        return self.default_value


class override_appsettings(override_settings):
    def __init__(self, appsetting, **kwargs):
        self.appsetting = appsetting
        super(override_appsettings, self).__init__(**kwargs)
        self.orig_settings = {}

    def enable(self):
        _values = self.appsetting._values
        for key, new_value in self.options.items():
            if not isinstance(new_value, Setting):
                new_value = MockSetting(new_value)
            #first make sure the setting is loaded
            getattr(self.appsetting, key)
            self.orig_settings[key] = _values[key]
            _values[key] = new_value

    def disable(self):
        _values = self.appsetting._values
        for key, orig_value in self.orig_settings.items():
            _values[key] = orig_value