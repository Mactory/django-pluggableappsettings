# -*- coding: utf-8 -*-
import logging

__author__ = 'Tim Schneider <tim.schneider@northbridge-development.de>'
__copyright__ = "Copyright 2015, Northbridge Development Konrad & Schneider GbR"
__credits__ = ["Tim Schneider", ]
__maintainer__ = "Tim Schneider"
__email__ = "mail@northbridge-development.de"
__status__ = "Release"

logger = logging.getLogger(__name__)

"""
This urlconf exists because Django expects ROOT_URLCONF to exist. URLs
should be added within the test folders, and use TestCase.urls to set them.
This helps the tests remain isolated.
"""

urlpatterns = []