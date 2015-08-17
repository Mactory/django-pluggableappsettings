[![PyPI version](https://badge.fury.io/py/django-pluggableappsettings.png)](http://badge.fury.io/py/django-pluggableappsettings) [![Build Status](https://travis-ci.org/NB-Dev/django-pluggableappsettings.svg?branch=master)](https://travis-ci.org/NB-Dev/django-pluggableappsettings) [![Coverage Status](https://coveralls.io/repos/NB-Dev/django-pluggableappsettings/badge.svg?branch=master)](https://coveralls.io/r/NB-Dev/django-pluggableappsettings?branch=master) [![Downloads](https://pypip.in/download/django-pluggableappsettings/badge.svg)](https://pypi.python.org/pypi/django-pluggableappsettings/) [![Supported Python versions](https://pypip.in/py_versions/django-pluggableappsettings/badge.svg)](https://pypi.python.org/pypi/django-pluggableappsettings/) [![License](https://pypip.in/license/django-pluggableappsettings/badge.svg)](https://pypi.python.org/pypi/django-pluggableappsettings/)
=====
django-pluggableappsettings
=====

This app provides a baseclass to easily realize AppSettings for any django project. The advantage of using an
AppSettings class lies in the possibility for the programmer to assign default values for settings if the setting is
not present in the main settings.py

Quick start
-----------

1. Install django-splitdate:
    * From the pip repository: ```pip install django-pluggableappsettings```
    * or directly from github: ```pip install git+git://github.com/NB-Dev/django-pluggableappsettings.git``

2. Create your AppSettings class in any of your project's files. E.g. in 'app_settings.py'.

3. Provide default values for any Setting you like by providing an attribute with the name '_DEFAULT_'<setting_name>
   in your AppSettings class

	```
	from django_pluggableappsettings import AppSettings
	
	class MyAppSettings(AppSettings):
		_DEFAULT_MY_SETTING = True
	```

4. Access the setting from anywhere:
	```
	from app_settings import MyAppSettings
	setting = MyAppSettings.MY_SETTING
	```

Default Values
----

Default values can either be fixed values or a callable function. If a callable function is provided, it will be called
without any parameters. If you use a static function, that is not bound to a class, you have to set it using the
```staticmethod``` function as it would otherwise be bound to your ```MyAppSettings``` class and not work. e.g.:

	```
	from django_pluggableappsettings import AppSettings
	
	def function():
		return 'Abc'
	
	class MyAppSettings(AppSettings):
		_DEFAULT_MY_SETTING = staticmethod(function)
	
	```

Accessing Values
----
You can access any setting by simply importing your AppSettings class and accessing the corresponding attribute. If the
corresponding setting is not set in the settings.py, it will fall back to the corresponding ```_DEFAULT_``` value. If
the ```__DEFAULT__``` value is not set, an ```AttributeError``` is raised.

Running the tests
----
The included tests can be run standalone by running the ```tests/runtests.py``` script. You need to have Django and
mock installed for them to run. If you also want to run coverage, you need to install it before running the tests
