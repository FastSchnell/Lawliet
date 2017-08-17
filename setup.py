# -*- coding: utf-8 -*-
"""
Lawliet
-------------
you can response json like this "return {}"
"""
from distutils.core import setup

setup(
    name='lawliet',
    version='2.4.3',
    description='a web framework for Python',
    author='Monomer Xu',
    author_email='fing@easymail.com.cn',
    url='https://github.com/fastschnell/Lawliet',
    py_modules=['lawliet'],
    packages=['lawliet', 'lawliet.handler', 'lawliet.tools'],
    license='MIT',
    platforms='any',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
