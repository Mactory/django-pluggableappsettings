# -*- coding: utf-8 -*-
import logging
import os

__author__ = 'Tim Schneider <tim.schneider@northbridge-development.de>'
__copyright__ = "Copyright 2015, Northbridge Development Konrad & Schneider GbR"
__credits__ = ["Tim Schneider", ]
__maintainer__ = "Tim Schneider"
__email__ = "mail@northbridge-development.de"
__status__ = "Development"

logger = logging.getLogger(__name__)


import pandoc

os.environ.setdefault('PYPANDOC_PANDOC', '/usr/local/bin/pandoc')

doc = pandoc.Document()
doc.markdown = open('README.md').read()
f = open('README.rst','w+')
f.write(doc.rst)
f.close()

os.system("python setup.py sdist")
os.system("twine upload --skip-existing dist/*")