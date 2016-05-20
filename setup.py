#!/usr/bin/env python
from setuptools import setup, find_packages

from httpbl import get_version

setup(
    name='django-httpbl',
    version=get_version(),
    url='https://github.com/regulusweb/django-httpbl',
    author="Regulus Ltd",
    author_email="reg@regulusweb.com",
    description=("Http:BL middleware for Django."),
    long_description='',
    keywords="Django, Http:BL",
    license="BSD",
    platforms=['linux'],
    packages=find_packages(),
    install_requires=[
        'django',
    ],
    extras_require={
    },
    # See http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Other/Nonlisted Topic'],
)
