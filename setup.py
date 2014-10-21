#!/usr/bin/env python
from setuptools import setup, find_packages

__version__ = "0.1"


setup(
    name="ychartspy",
    author="Gregory Rehm",
    version=__version__,
    description="Python Client for YCharts",
    packages=find_packages(exclude=["*.tests"]),
    package_data={"*": ["*.html"]},
    install_requires=[
        "requests",
    ],
    tests_require=[
        "mock",
        "nose"
    ]
)
