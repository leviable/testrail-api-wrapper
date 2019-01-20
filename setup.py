from __future__ import absolute_import
from setuptools import find_packages, setup
from os.path import dirname, join, realpath

HERE = dirname(realpath(__file__))

try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError

try:
    with open(join(HERE, 'traw', 'VERSION'), 'r') as r:
        version = r.read()
except FileNotFoundError:
    version = '0.0.0'

with open(join(HERE, 'README.rst'), 'r') as r:
    long_description = r.read()

setup(
    name="traw",
    author="Levi Noecker",
    author_email="levi.noecker@gmail.com",
    url="https://github.com/levi-rs/testrail-api-wrapper",
    description="Python library and CLI for interfacing with TestRail's REST API",
    long_description=long_description,
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    version=version,
    install_requires=['click', 'requests', 'retry', 'singledispatch', 'six'],
    keywords="testrail client api wrapper traw",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    entry_points={
        'console_scripts': [
            'traw=traw.cli:cli',
        ]
    }
)
