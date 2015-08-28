# -*- coding: utf-8 -*-
from __future__ import absolute_import
import logging
from django.test import TestCase, override_settings
from mock import  MagicMock
from django_pluggableappsettings import AppSettings, Setting, CallableSetting, ClassSetting, NOT_SET_VALUE

__author__ = 'Tim Schneider <tim.schneider@northbridge-development.de>'
__copyright__ = "Copyright 2015, Northbridge Development Konrad & Schneider GbR"
__credits__ = ["Tim Schneider", ]
__maintainer__ = "Tim Schneider"
__email__ = "mail@northbridge-development.de"
__status__ = "Development"

logger = logging.getLogger(__name__)

function_mock = MagicMock(return_value='Function')

class TestClass(object):
    pass

class TestAppSettings(AppSettings):
    SETTING = Setting('Default')

class TestAppSettingsTestCase(TestCase):
    def tearDown(self):
        TestAppSettings._values = {}

    def setUp(self):
        self.values = {}
        TestAppSettings._values = self.values


class AppSettingsTestCase(TestAppSettingsTestCase):
    def test_access_of_non_existing_setting(self):
        try:
            TestAppSettings.NON_EXISTENT
            self.fail()
        except AttributeError:
            pass
        except:
            self.fail()

    def test_access_of_existing_value_from_values(self):
        self.values['NON_EXISTENT'] = 'FOUND'

        self.assertEqual(TestAppSettings.NON_EXISTENT, 'FOUND')

    def values_stored_in_dict(self):
        mocked = MagicMock(get=MagicMock(return_value='GET'))
        TestAppSettings.MOCK = mocked
        self.assertEqual(TestAppSettings.MOCK, 'GET')
        self.assertEqual(self.values['MOCK'], 'GET')

    @override_settings(SETTING='Setting')
    def test_get_value_from_settings(self):
        self.assertEqual(TestAppSettings.SETTING, 'Setting')

class SettingTestCase(TestCase):
    def test___init__(self):
        setting = Setting('default')
        self.assertEqual(setting.default_value, 'default')

        setting = Setting(default_value='default')
        self.assertEqual(setting.default_value, 'default')

    def test_get_no_setting_no_default(self):
        setting = Setting()
        self.assertRaisesMessage(
            AttributeError,
            "The setting SETTING is not defined in your settings.py and no default value is provided.",
            setting.get,
            'SETTING',
            NOT_SET_VALUE
        )

    def test_get_default(self):
        setting = Setting('default')
        val = setting.get('SETTING', NOT_SET_VALUE)
        self.assertEqual(val, 'default')

    def test_get_settings_value(self):
        setting = Setting('default')
        val = setting.get('SETTING', 'settings_value')
        self.assertEqual(val, 'settings_value')

class CallableSettingTestCase(TestCase):
    def test_get_not_callable(self):
        setting = CallableSetting()
        value = setting.get('SETTING', 'String')
        self.assertEqual(value, 'String')

    def test_get_callable(self):
        setting = CallableSetting()
        value = setting.get('SETTING', MagicMock(return_value='Called'))
        self.assertEqual(value, 'Called')

class ClassSettingTestCase(TestCase):
    def test_no_class_or_string(self):
        setting = ClassSetting()
        self.assertRaisesMessage(
            ValueError,
            'The value for the setting SETTING either has to be a class or a string containing the dotted path of a class.',
            setting.get,
            'SETTING',
            1
        )

    def test_wrong_dotted_path(self):
        setting = ClassSetting()
        self.assertRaisesMessage(
            ValueError,
            'The class described by "does.not.exist" for the setting SETTING could not be found.',
            setting.get,
            'SETTING',
            'does.not.exist'
        )

    def test_class(self):
        setting = ClassSetting()
        value = setting.get('SETTING', TestClass)
        self.assertEqual(value, TestClass)

    def test_dotted_class(self):
        setting = ClassSetting()
        value = setting.get('SETTING', 'django_pluggableappsettings.tests.test___init__.TestClass')
        self.assertEqual(value, TestClass)
