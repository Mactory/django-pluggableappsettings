# -*- coding: utf-8 -*-
from __future__ import absolute_import
import logging
from django.test import TestCase, override_settings
from mock import  MagicMock
from django_pluggableappsettings import AppSettings

__author__ = 'Tim Schneider <tim.schneider@northbridge-development.de>'
__copyright__ = "Copyright 2015, Northbridge Development Konrad & Schneider GbR"
__credits__ = ["Tim Schneider", ]
__maintainer__ = "Tim Schneider"
__email__ = "mail@northbridge-development.de"
__status__ = "Development"

logger = logging.getLogger(__name__)

function_mock = MagicMock(return_value='Function')

class TestAppSettings(AppSettings):
    _DEFAULT_VALUE = "Attribute"
    _DEFAULT_FUNCTION = function_mock

class AppSettingsTestCase(TestCase):

    def tearDown(self):
        if hasattr(TestAppSettings, 'VALUE'):
            del TestAppSettings.VALUE
        if hasattr(TestAppSettings, 'FUNCTION'):
            del TestAppSettings.FUNCTION
        function_mock.reset_mock()

    def test_access_of_non_existent_attribute(self):
        try:
            TestAppSettings.NON_EXISTENT
            self.fail()
        except AttributeError:
            pass
        except:
            self.fail()

    def test_access_of_attribute_default_value(self):
        self.assertEqual(TestAppSettings.VALUE, "Attribute")

    @override_settings(VALUE='Custom')
    def test_access_of_attribute_set_value(self):
        self.assertEqual(TestAppSettings.VALUE, "Custom")


    def test_access_of_attribute_default_function(self):
        self.assertEqual(TestAppSettings.FUNCTION, 'Function')
        function_mock.assert_called_once_with()
