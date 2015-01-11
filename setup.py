#! /usr/bin/env python
#
# Tastypie Searchable via Haystack
# ======================================================================
try:
    # Allow Python eggs bdist_egg
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from tastypie_searchable import __version__

readme = open('README.md', 'r')
README_TEXT = readme.read()
readme.close()

setup(name='django-tastypie-searchable',
      version=__version__,
      license='MIT Licensed',
      description='Tastypie Full-Text Searchable ModelResource via Haystack',
      long_description=README_TEXT,
      author='Andrew Droffner',
      author_email='adroffner@gmail.com',
      url='https://github.com/adroffner/tastypie-searchable',
      download_url='',
      packages=['tastypie_searchable', ],
      ## scripts=[''],
      requires=[
          'django>=1.5',
          'django-haystack>=2.0',
          'queued_search',
      ],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          ],
     )


