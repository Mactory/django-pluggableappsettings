|PyPI version| |Build Status| |Coverage Status| |Downloads| |Supported Python versions| |License|
=================================================================================================

django-appsettings
================

This app provides a baseclass to easily realize AppSettings for any django project. The advantage of using an
AppSettings class lies in the possibility for the programmer to assign default values for settings if the setting is
not present in the main settings.py

Quick start
-----------

1. Install django-app-settings:

   -  From the pip repository: ``pip install django_appsettings``
   -  or directly from github:
      \`\ ``pip install git+git://github.com/NB-Dev/django-appsettings.git``

2. Create your AppSettings class e.g. in ``app_settings.py``:



Global Configuration
--------------------

The SplitDateField can be configured globally in your settings.py file
with the following options

SPLITDATE\_ORDER (String or Dict):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Defines the ordering of the day, month and year fields.

The order of the fields is defined by a three character string, that
contains the characters 'd'(day), 'm'(month), 'y'(year) in the desired
order.

The setting can either be such a string to be used on each
SplitDateField no matter what language is selected, or a dictionary
containing key, value pairs with a locale name as key and the
corresponding order string as value to be used depending on the current
locale

Default:

::

        dict((
            ('en', 'mdy'),
            ('de', 'dmy')
        ))

SPLITDATE\_PLACEHOLDER\_DAY (String):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A string defining the placeholder of the day field.

Default: ``_('DD')``

SPLITDATE\_PLACEHOLDER\_MONTH (String):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A string defining the placeholder of the month field.

Default: ``_('MM')``

SPLITDATE\_PLACEHOLDER\_YEAR (String):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A string defining the placeholder of the year field.

Default: ``_('YYYY')``

Widget configuration
--------------------

If you want to customize the widget of the SplitDateField, use the
SplitDateWidget.

e.g. add a class:

::

    from django_splitdate.forms import SplitDateField, SplitDateWidget
        date = forms.SplitDateField(widget=SplitDateWidget(attrs={'class':'myclass'}))

Additionally the widget takes the following local overwrites of the
global configurations at initialization:

field\_ordering (String or Dict):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Local overwrite for SPLITDATE\_ORDER. Possible values, see above.

placeholder\_day (String):
^^^^^^^^^^^^^^^^^^^^^^^^^^

Local overwrite for SPLITDATE\_PLACEHOLDER\_DAY. Possible values, see
above.

placeholder\_month (String):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Local overwrite for SPLITDATE\_PLACEHOLDER\_MONTH. Possible values, see
above.

placeholder\_year (String):
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Local overwrite for SPLITDATE\_PLACEHOLDER\_YEAR. Possible values, see
above.

Running the tests
-----------------

The included tests can be run standalone by running the
``tests/runtests.py`` script. The only requirement for this is Django >=
1.7. If you also want to run coverage, you need to install it before
running the tests

.. |PyPI version| image:: https://badge.fury.io/py/django-splitdate.png
   :target: http://badge.fury.io/py/django-splitdate
.. |Build Status| image:: https://travis-ci.org/NB-Dev/django-splitdate.svg?branch=master
   :target: https://travis-ci.org/NB-Dev/django-splitdate
.. |Coverage Status| image:: https://coveralls.io/repos/NB-Dev/django-splitdate/badge.svg?branch=master
   :target: https://coveralls.io/r/NB-Dev/django-splitdate?branch=master
.. |Downloads| image:: https://pypip.in/download/django-splitdate/badge.svg
   :target: https://pypi.python.org/pypi/django-splitdate/
.. |Supported Python versions| image:: https://pypip.in/py_versions/django-splitdate/badge.svg
   :target: https://pypi.python.org/pypi/django-splitdate/
.. |License| image:: https://pypip.in/license/django-splitdate/badge.svg
   :target: https://pypi.python.org/pypi/django-splitdate/
