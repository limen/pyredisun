#!/usr/bin/env python

from setuptools import setup

setup(name='redisun',
      version='0.1',
      author='LI Mengxiang',
      author_email='limengxiang876@gmail.com',
      maintainer='LI Mengxiang',
      maintainer_email='limengxiang876@gmail.com',
      url='https://github.com/limen/redisun-py',
      description='Make Redis manipulations easy, unify commands for all data types',
      packages=['redisun'],
      install_requires=[
        'redis',
      ],
      test_requires=[
        'pytest',
      ],
      license='MIT',
      platforms=['any'],
     )
