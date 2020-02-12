[![PyPI version](https://img.shields.io/pypi/v/django-pluggableappsettings.svg)](http://badge.fury.io/py/django-pluggableappsettings) [![Build Status](https://travis-ci.org/NB-Dev/django-pluggableappsettings.svg?branch=master)](https://travis-ci.org/NB-Dev/django-pluggableappsettings) [![Coverage Status](https://coveralls.io/repos/NB-Dev/django-pluggableappsettings/badge.svg?branch=master&service=github)](https://coveralls.io/github/NB-Dev/django-pluggableappsettings?branch=master) [![Supported Python versions](https://img.shields.io/pypi/pyversions/django-pluggableappsettings.svg)](https://pypi.python.org/pypi/django-pluggableappsettings/) [![Supported Django versions](https://img.shields.io/badge/Django-1.6%2C%201.7%2C%201.8%2C%201.9%2C%201.10%2C%201.11%2C%202.0-brightgreen.svg)](https://pypi.python.org/pypi/django-pluggableappsettings/) [![License](https://img.shields.io/pypi/l/django-pluggableappsettings.svg)](https://pypi.python.org/pypi/django-pluggableappsettings/) [![Codacy Badge](https://api.codacy.com/project/badge/grade/79d4fa62bb77478392d9535067d010c6)](https://www.codacy.com/app/tim_11/django-pluggableappsettings) [![Requirements Status](https://requires.io/github/NB-Dev/django-pluggableappsettings/requirements.svg?branch=master)](https://requires.io/github/NB-Dev/django-pluggableappsettings/requirements/?branch=master)



# django-pluggableappsettings


This app provides a baseclass to easily realize AppSettings for any django project. The advantage of using an
AppSettings class lies in the possibility for the programmer to assign default values for settings if the setting is
not present in the main settings.py

## Requirements:

* Django >= 2.0

## Quick start

1. Install django-pluggableappsettings
    * From the pip repository: ```pip install django-pluggableappsettings```
    * or directly from github: ```pip install git+git://github.com/NB-Dev/django-pluggableappsettings.git```

2. Create your AppSettings class in any of your project's files. E.g. in 'app_settings.py'.

3. Define your settings by setting the class attributes as one of the provided settings types

	```
	from django_pluggableappsettings import AppSettings, Setting
	
	class MyAppSettings(AppSettings):
		MY_SETTING = Setting('DEFAULT_VALUE')
	```

4. Access the setting from anywhere:
	```
	from app_settings import MyAppSettings
	setting = MyAppSettings.MY_SETTING
	```

## Provided Setting Types

Different setting types are provided with the package:

### Setting(default_value, setting_name, aliases)

The most basic setting that looks up the setting's value from the `settings.py` usually the attribute name is used for
the detection. If, however, the `settings_name` parameter is given, this name is used instead for the lookup in the
`settings.py`. It simply returns the value from the settings.py or, if that is not set, the default value.
If no default value is provided and the setting is not set in your settings.py, an ```AttributeError``` is thrown.
Also a list of aliases can be passed to allow for multiple names of one setting (e.g. for backwards compatibility)


### CalledOnceSetting(default_value, setting_name, aliases, force_callable=False)

Checks whether the value is callable and calls it once before returning. Subsequent accesses to this setting return the
cached return value of the first call. If `force_callable` is `True`, the setting throws a `ValueError` if the value of
the setting is not callable.


### CalledEachTimeSetting(default_value, setting_name, aliases, force_callable=False)

Checks whether the value is callable. If so, the callable is called each time when the setting is
accessed. If `force_callable` is `True`, the setting throws a `ValueError` if the value of the setting is not callable.


### ClassSetting(default_value, setting_name, aliases)

Behaves as a Setting but accepts only Classes or dotted paths to classes as values. If the value is a dotted path, the
path is translated to a class before returning, so the returned value is always a class.

### IntSetting(default_value, setting_name, aliases)

Accepts only values that are of type int or can be casted to type int

### FloatSetting(default_value, setting_name, aliases)

Accepts only values of type float of values that can be casted to type float

### StringSetting(default_value, setting_name, aliases)

Accepts only strings as value

### IterableSetting(default_value, setting_name, aliases)

Makes sure that the value is an iterable

### TypedSetting(default_value, setting_name, aliases)

A class that checks whether the given value is of a certain type and optionally allows casting the value to that type.
Used as a base class for all type checking classes and can be easily subclassed to allow checking of various
value types.

To create your own type checking setting simply subclass this type and set the class attributes `_setting_type`
and `_cast_value` according to your needs. The `_setting_type` attribute specifies the desired type while the
`_cast_value` attribute specifies whether the value should be casted to the `_setting_type`. A `_cast_value`
of `True` essentially results in a call of `value = _setting_type(value)`.

E.g. The `IntSetting` is defined as follows:
```
class IntSetting(TypedSetting):
    """
    An integer setting
    """
    _setting_type = int
    _cast_value = True
```

If you need more elaborate casting functions, you can overwrite the `cast_value(self, value)` function
of your type which should return the casted value.

## Accessing Values

You can access any setting by simply importing your AppSettings class and accessing the corresponding attribute. 

## Tests with AppSettings

The package provides a convenient `override_appsettings` decorator / context manager to allow for the temporary
override of AppSettings values. It is used just like Django's `override_settings` decorator but with an extra argument:
The AppSettings-Class that is to be altered has to be passed in as first argument. Following should be keyword, value
arguments where the keyword is the name of the setting to be overridden and the value is the desired return value.

E.g.:
```
from django_pluggableappsettings.test.utils import override_appsettings
from myapp.appsettings import MyAppSettings

class SomeTestCase(TestCase):
    @override_appsettings(MyAppSettings, SETTING='new_value')
    def test_decorated(self):
        MyAppSettings.SETTING # This returns 'new_value'
    
    def test_context_manager(self):
        with override_appsettings(MyAppSettings, SETTING='new_value'):
            MyAppSettings.SETTING # This returns 'new_value'

```

## Running the tests

The included tests can be run standalone by running the `tests/runtests.py` script. You need to have Django and
mock installed for them to run. If you also want to run coverage, you need to install it before running the tests


## CHANGELOG

### v. 2.0.0 (2020-02-12)
- Breaking Change: Dropping Support for Python 2. Results in a dropping of support for Django 1.x.
- Addings Upport for Django 2.1, 2.2 and 3.0


### v. 1.1.6 (2017-05-19)
- Fixing the README to be correctly displayed on pypi

### v. 1.1.5 (2017-05-19)
- Version bump as I forgot to convert the readme. Added a publish.py to automate publishing in future.

### v. 1.1.4 (2017-05-19)
- Adding tests for Django 1.10 and 1.11.

### v. 1.1.3 (2016-01-27)
- Adding the possibility to look for a settings value under a different name in the `settings.py` by usage of the
`settings_name` parameter
- Fixing a bug that caused all `AppSettings` instances to share the same cache of loaded settings. This could cause the
settings to be overridden by other settings 

### v. 1.1.2 (2016-01-15)
- Adding an `override_appsettings` decorator / context manager to allow the overriding of AppSettings values in test
- Added the possibility to retrieve non-`Setting` attributes from the `AppSettings` class to allow for custom attributes
 or custom functions.

### v.1.1.1
- I screwed up with pypi and need to bump the version number - Sorry

### v.1.1.0
- Changing structure of Setting class to being able to add repeatedly called functions as setting.
 
 **Warning**: This breaks compatibility of custom settings classes. To fix this, simply rename the `get` method of
 your custom classes to `_get`
- Added a `CalledEachTimeSetting` that takes a callable that is called each time the setting's value is accessed
- Renamed the `CallableSetting` to `CalledOnceSetting` to make the differentiation to the `CalledEachTimeSetting`
 clearer. The old name will stay as an alias for now.
- The `CalledEachTimeSetting` and the `CalledOnceSetting` take an `force_callable` kwarg to set whether the value of the
setting is enforced to be callable or not.

### v.1.0.0
- Releasing first stable version

### v.0.2.3
- Added 'aliases' parameter to ```Setting``` to allow multiple names for one setting (e.g. for backwards compatibility)

### v.0.2.2
- Extended code to also work with Python 3

### v.0.2.1
- Added ```TypedSetting``` Setting type which allows for the setting to be typechecked
- Added ```IntSetting```, ```FloatSetting```, ```StringSetting``` and ``ÌterableSetting``` as subtypes of ```TypedSetting``

### v.0.2.0

- Added the changelog
- Redesign of settings to allow different types of settings that can now also provide type checking.
- Settings are now explicitly defined and no ```_DEFAULT_``` prefix is needed anymore
- Also no staticmethod decorator is needed anymore

## ToDos:
- Allow the easy definition of multiple allowed setting types so that a setting could e.g. accept either string or an
Integer
- Allow the chaining of callables with typed settings to check that the return value of a callable is of the correct
type

## Maintainers
This Project is maintaned by [Pay-Per-X](https://www.pay-per-x.com)
