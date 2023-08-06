# -*- coding: utf-8 -*-

"""

    Module :mod:``


    LICENSE: The End User license agreement is located at the entry level.

A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# To use a consistent encoding
from os import path

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

setup(
    name='orm.base',
    version='1.0.0',
    description='',
    author='Siva Cn',
    author_email='cnsiva@protonmail.com',
    project_urls={
        'Source': 'https://github.com/SivaCn/orm.base',
    },
    license='MIT',
    platforms='any',
    # Classifiers help users find your project by categorizing it.
    #
    # For a list of valid classifiers, see
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    namespace_packages=['orm', 'orm.base'],

    # Install dependencies
    python_requires=">=2.7",
    install_requires=[
        "sqlalchemy>=1.2.19",
    ],

    # Console script entry points
    entry_points={},
)
