#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

__author__ = 'Tim Schneider <tim.schneider@northbridge-development.de>'
__copyright__ = "Copyright 2015, Northbridge Development Konrad & Schneider GbR"
__credits__ = ["Tim Schneider", ]
__maintainer__ = "Tim Schneider"
__email__ = "mail@northbridge-development.de"
__status__ = "Release"

logger = logging.getLogger(__name__)


import glob
import os
import sys
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
print BASE_DIR
sys.path.insert(0, os.path.abspath(BASE_DIR))

try:
    import coverage # Import coverage if available
    cov = coverage.coverage(
        cover_pylib=False,
        config_file=os.path.join(os.path.dirname(__file__), 'coverage.conf'),
        include='%s/*' % BASE_DIR,
    )
    cov.start()
    sys.stdout.write('Using coverage\n')
except ImportError:
    cov = None
    sys.stdout.write('Coverage not available. To evaluate the coverage, please install coverage.\n')

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

django.setup()
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

if cov is not None:
    sys.stdout.write('Evaluating Coverage\n')
    cov.stop()
    cov.save()
    sys.stdout.write('Generating HTML Report\n')
    cov.html_report()