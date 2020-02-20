#!/usr/bin/env python

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='tap-google-my-business',
      version='1.0.0',
      description='Singer Tap for Google My Business API',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='360 Agency',
      url='https://github.com/ReptilianBrain/tap-google-my-business',
      classifiers=[
          'Programming Language :: Python :: 3 :: Only'
      ],
      py_modules=['tap_google_my_business'],
      install_requires=[
          'singer-python==5.9.0',
          'google-api-python-client==1.7.11',
          'oauth2client==4.1.3'
      ],
      entry_points='''
          [console_scripts]
          tap-google-my-business=tap_google_my_business:main
      ''',
      packages=['tap_google_my_business'],
      package_data={
          'tap_google_my_business/defaults': [
              "default_catalog.json",
          ],
      },
      include_package_data=True,

      )
