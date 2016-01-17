"""
Lawliet
-------------
you can response json like this "return {}"
"""
from setuptools import setup

setup(
    name='lawliet',
    version='2.1.0',
    description='a web framework',
    long_description='a web framework',
    author='Monomer Xu',
    author_email='fing@easymail.com.cn',
    url='https://github.com/fing520/Lawliet',
    py_modules=['lawliet'],
    packages=['lawliet'],
    license='MIT',
    zip_safe=False,
    include_package_data=True,
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
