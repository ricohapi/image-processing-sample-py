# -*- coding: utf-8 -*-
# Copyright (c) 2016 Ricoh Co., Ltd. All Rights Reserved.

from setuptools import setup, find_packages

setup(
    name='ricohapi-ips',
    version='1.0.0',
    description='Ricoh-image-processing-sample for Python',
    long_description="""Ricoh Image Processing Sample for Python""",
    author='Ricoh',
    url='https://github.com/ricohapi/image-processing-sample-py',
    classifiers=[
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'requests',
        'Pillow',
    ],
    test_suite='nose.collector',
    tests_require=['nose', 'mock', 'coverage'],
)
