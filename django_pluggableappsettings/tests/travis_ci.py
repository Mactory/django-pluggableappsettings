#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

__author__ = 'Tim Schneider <tim.schneider@northbridge-development.de>'
__copyright__ = "Copyright 2015, Northbridge Development Konrad & Schneider GbR"
__credits__ = ["Tim Schneider", ]
__maintainer__ = "Tim Schneider"
__email__ = "mail@northbridge-development.de"
__status__ = "Development"

logger = logging.getLogger(__name__)


import glob
import os
import sys
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, os.path.abspath(BASE_DIR))

import django
from django.conf import settings
from django.core.management import execute_from_command_line



# Unfortunately, apps can not be installed via ``modify_settings``
# decorator, because it would miss the database setup.
INSTALLED_APPS = (
)

settings.configure(
    SECRET_KEY="django_tests_secret_key",
    DEBUG=False,
    TEMPLATE_DEBUG=False,
    ALLOWED_HOSTS=[],
    INSTALLED_APPS=INSTALLED_APPS,
    MIDDLEWARE_CLASSES=[],
    ROOT_URLCONF='tests.urls',
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
        }
    },
    LANGUAGE_CODE='en-us',
    TIME_ZONE='UTC',
    USE_I18N=True,
    USE_L10N=True,
    USE_TZ=True,
    STATIC_URL='/static/',
    # Use a fast hasher to speed up tests.
    PASSWORD_HASHERS=(
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ),
    FIXTURE_DIRS=glob.glob(BASE_DIR + '/' + '*/fixtures/')

)

try:
    # Django >=1.7 needs this, but other versions dont.
    django.setup()
except AttributeError:
    pass

args = [sys.argv[0], 'test']
# Current module (``tests``) and its submodules.
test_cases = '.'

# Allow accessing test options from the command line.
offset = 1
try:
    sys.argv[1]
except IndexError:
    pass
else:
    option = sys.argv[1].startswith('-')
    if not option:
        test_cases = sys.argv[1]
        offset = 2

args.append(test_cases)
# ``verbosity`` can be overwritten from command line.
#args.append('--verbosity=2')
args.extend(sys.argv[offset:])

execute_from_command_line(args)
