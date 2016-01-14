# -*- coding: utf-8 -*-
from __future__ import absolute_import
import logging
from django.test import TestCase
from django.test.utils import override_settings
from mock import patch
from django_pluggableappsettings import AppSettings, Setting
from django_pluggableappsettings.test.utils import MockSetting, override_appsettings

__author__ = 'Tim Schneider <tim.schneider@northbridge-development.de>'
__copyright__ = "Copyright 2016, Northbridge Development Konrad & Schneider GbR"
__credits__ = ["Tim Schneider", ]
__maintainer__ = "Tim Schneider"
__email__ = "mail@northbridge-development.de"
__status__ = "Development"

logger = logging.getLogger(__name__)

class MockSettingTestCase(TestCase):
    @patch('django_pluggableappsettings.Setting.__init__')
    def test___init__(self, __init__):
        MockSetting('value')
        __init__.assert_called_once_with('value')

    def test__get_value(self):
        s = MockSetting('value')
        self.assertEqual(s._get_value(), 'value')


class TestAppSettings(AppSettings):
    SETTING = Setting('Value')


class override_appsettingsTestCase(TestCase):
    @override_settings(SETTING='Custom value')
    def test_decorator(self):
        @override_appsettings(TestAppSettings, SETTING='Overridden')
        def decorated():
            return TestAppSettings.SETTING

        #value before
        self.assertEqual(TestAppSettings.SETTING, 'Custom value')

        #overridden
        self.assertEqual(decorated(), 'Overridden')

        #value after
        self.assertEqual(TestAppSettings.SETTING, 'Custom value')

    @override_settings(SETTING='Custom value')
    def test_context_processor(self):
        #value before:
        self.assertEqual(TestAppSettings.SETTING, 'Custom value')
        with override_appsettings(TestAppSettings, SETTING='Overridden'):
            #overridden
            self.assertEqual(TestAppSettings.SETTING, 'Overridden')

        #value after:
        self.assertEqual(TestAppSettings.SETTING, 'Custom value')
