#! /usr/bin/env python
#
# Tastypie Searchable ModelResource Objects
# ======================================================================
try:
    # Allow Python eggs bdist_egg
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from tastypie_search import __version__

readme = open('README.md', 'r')
README_TEXT = readme.read()
readme.close()

setup(name='django-tastypie-searchable',
      version=__version__,
      license='MIT Licensed',
      description='Tastypie Searchable ModelResource using Haystack',
      long_description=README_TEXT,
      author='Andrew Droffner',
      author_email='adroffner@gmail.com',
      url='https://github.com/adroffner/tastypie-searchable',
      download_url='',
      packages=['tastypie_search', ],
      ## scripts=[''],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          ## 'Programming Language :: Python :: 2.6', # import importlib in signals.py is 2.7 or greater.
          'Programming Language :: Python :: 2.7',
          ],
     )

