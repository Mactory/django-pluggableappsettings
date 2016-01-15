# -*- coding: utf-8 -*-
from __future__ import absolute_import
import logging

from django.test import TestCase

try:
    from django.test import override_settings
except ImportError:
    from django.test.utils import override_settings
from mock import MagicMock, patch
from django_pluggableappsettings import AppSettings, Setting, ClassSetting, NOT_SET_VALUE, TypedSetting, \
    CalledOnceSetting, CalledBaseSetting, CallableSetting, CalledEachTimeSetting

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
    SETTING = Setting('Default',aliases=['ALIAS','ALIAS2'])



class TestAppSettingsTestCase(TestCase):
    def tearDown(self):
        TestAppSettings._values = {}

    def setUp(self):
        self.values = {}
        TestAppSettings._values = self.values

class AppSettingsTestCase(TestAppSettingsTestCase):
    def test_access_of_non_existing_setting(self):
        '''
        Test whether an Attribute Error is thrown if a non existent setting is accessed
        :return:
        '''
        try:
            TestAppSettings.NON_EXISTENT
            self.fail()
        except AttributeError:
            pass
        except:
            self.fail()

    def test_access_of_non_settings(self):
        '''
        Test whether non Setting attributes can be accessed
        :return:
        '''
        id_object = object()
        TestAppSettings.test_obj = id_object

        self.assertEqual(TestAppSettings.test_obj, id_object)

    def test_access_of_existing_value_from_values(self):
        '''
        Test whether a Setting stored in the values dictionary receives prominence over the configured Setting, a.k.a
        wheter a once loaded setting is not loaded again
        :return:
        '''
        self.values['SETTING'] = MagicMock(value=MagicMock(return_value='FOUND'))
        self.assertEqual(TestAppSettings.SETTING, 'FOUND')

    def values_stored_in_dict(self):
        '''
        Test whether a Setting is saved in the values dictionary after it's first access
        :return:
        '''
        mocked = MagicMock(_get=MagicMock(return_value='GET'), _value=MagicMock(return_value='GET'))
        TestAppSettings.MOCK = mocked
        self.assertEqual(TestAppSettings.MOCK, 'GET')
        self.assertEqual(self.values['MOCK'], mocked)

    @override_settings(SETTING='Setting')
    def test_get_value_from_settings(self):
        '''
        Test whether a value can be accessed
        :return:
        '''
        self.assertEqual(TestAppSettings.SETTING, 'Setting')

    def test_alias_setting(self):
        '''
        Test whether a value can be accessed by an alias
        :return:
        '''
        with override_settings(ALIAS='Alias'):
            self.assertEqual(TestAppSettings.SETTING, 'Alias')

        TestAppSettings._values = {}
        with override_settings(ALIAS2='Alias2'):
            self.assertEqual(TestAppSettings.SETTING, 'Alias2')



class SettingTestCase(TestCase):
    def test___init__(self):
        setting = Setting('default')
        self.assertEqual(setting.default_value, 'default')

        setting = Setting(default_value='default')
        self.assertEqual(setting.default_value, 'default')

        # test alias_possibilities
        setting = Setting(aliases='abc')
        self.assertEqual(setting._aliases, ['a', 'b', 'c'])

        setting = Setting(aliases=('abc', 1, 3))
        self.assertEqual(setting._aliases, ['abc'])

        setting = Setting(aliases=1)
        self.assertEqual(setting._aliases, [])


    def test__get_no_setting_no_default(self):
        setting = Setting()
        self.assertRaisesMessage(
            AttributeError,
            "The setting SETTING is not defined in your settings.py and no default value is provided.",
            setting._get,
            'SETTING',
            NOT_SET_VALUE
        )

    def test__get_default(self):
        setting = Setting('default')
        val = setting._get('SETTING', NOT_SET_VALUE)
        self.assertEqual(val, 'default')

    def test__get_settings_value(self):
        setting = Setting('default')
        val = setting._get('SETTING', 'settings_value')
        self.assertEqual(val, 'settings_value')

    def test_get(self):
        with patch('django_pluggableappsettings.Setting._get', MagicMock(return_value=42)) as _get:
            setting = Setting('default')
            setting.get('SETTING', 'settings_value')
            self.assertEqual(setting._value, 42)
            _get.assert_called_with('SETTING', 'settings_value')

    def test__get_value(self):
        setting = Setting('default')

        #raises error without a value set
        self.assertRaises(RuntimeError, setting._get_value)


        #returns value if it is set
        id_object = object()
        setting._value = id_object
        self.assertEqual(setting._get_value(), id_object)

    def test_value(self):
        id_object = object()
        with patch('django_pluggableappsettings.Setting._get_value', MagicMock(return_value=id_object)) as _get_value:
            setting = Setting('default')
            self.assertEqual(setting.value(), id_object)
            _get_value.assert_called_with()

class CalledBaseSettingTestCase(TestCase):
    def test___init__(self):
        setting = CalledBaseSetting(force_callable=True)
        self.assertTrue(setting._force_callable)

        setting = CalledBaseSetting(force_callable=False)
        self.assertFalse(setting._force_callable)

    def test__get_not_callable(self):
        setting = CalledBaseSetting(force_callable=True)
        self.assertRaises(
            ValueError,
            setting._get,
            'SETTING',
            'String'
        )
        setting = CalledBaseSetting(force_callable=False)
        self.assertEqual(setting._get('SETTING', 'String'), 'String')

    def test__get_callable(self):
        setting = CalledBaseSetting()
        mock = MagicMock(return_value='Called')
        value = setting._get('SETTING', mock)
        self.assertEqual(value, mock)

class CalledOnceSettingTestCase(TestCase):

    def test__get_callable(self):
        setting = CalledOnceSetting()
        value = setting._get('SETTING', MagicMock(return_value='Called'))
        self.assertEqual(value, 'Called')

    def test__get_not_callable(self):
        setting = CalledOnceSetting(force_callable=False)
        self.assertEqual(setting._get('SETTING', 'String'), 'String')

class CallableSettingTestCase(TestCase):

    def test___init__(self):
        CallableSetting()

class CalledEachTimeSettingTestCase(TestCase):

    def test__get_value_callable(self):
        setting = CalledEachTimeSetting()
        id_object = object()
        with patch('django_pluggableappsettings.CalledBaseSetting._get_value', MagicMock(return_value=MagicMock(return_value=id_object))) as _get_value:
            value = setting._get_value()
            self.assertEqual(value, id_object)

    def test__get_value_not_callable(self):
        setting = CalledEachTimeSetting(force_callable=False)
        id_object = object()
        with patch('django_pluggableappsettings.CalledBaseSetting._get_value', MagicMock(return_value=id_object)) as _get_value:
            value = setting._get_value()
            self.assertEqual(value, id_object)

class ClassSettingTestCase(TestCase):
    def test_no_class_or_string(self):
        setting = ClassSetting()
        self.assertRaisesMessage(
            ValueError,
            'The value for the setting SETTING either has to be a class or a string containing the dotted path of a class.',
            setting._get,
            'SETTING',
            1
        )

    def test_wrong_dotted_path(self):
        setting = ClassSetting()
        self.assertRaisesMessage(
            ValueError,
            'The class described by "does.not.exist" for the setting SETTING could not be found.',
            setting._get,
            'SETTING',
            'does.not.exist'
        )

    def test_class(self):
        setting = ClassSetting()
        value = setting._get('SETTING', TestClass)
        self.assertEqual(value, TestClass)

    def test_dotted_class(self):
        setting = ClassSetting()
        value = setting._get('SETTING', 'django_pluggableappsettings.tests.test___init__.TestClass')
        self.assertEqual(value, TestClass)

class TypedSettingTestCase(TestCase):
    def test_cast_value(self):
        class MockTypedSetting(TypedSetting):
            _setting_type = MagicMock(return_value='casted')
            _cast_value = False
        setting = MockTypedSetting()
        ret = setting.cast_value('test')
        self.assertEqual(ret, 'test')
        setting._setting_type.assert_not_called()

        setting._cast_value = True
        ret = setting.cast_value('test')
        self.assertEqual(ret, 'casted')
        setting._setting_type.assert_called_once_with('test')

    def test_get_value(self):
        class MockTypedSetting(TypedSetting):
            pass
        setting = MockTypedSetting()

        # No _setting_type
        self.assertRaises(AttributeError, setting._get, 'SETTING', 'val')

        setting._setting_type = int

        #wrong type error
        self.assertRaisesMessage(ValueError, 'The value for setting SETTING is not of type int', setting._get, 'SETTING', 'val')

        setting._cast_value = True

        #cast error

        self.assertRaisesMessage(ValueError, 'The value for setting SETTING cannot be casted to type int', setting._get, 'SETTING', 'val')

        # No error
        self.assertEqual(setting._get('SETTING', 1), 1)
        self.assertEqual(setting._get('SETTING', '1'), 1)
