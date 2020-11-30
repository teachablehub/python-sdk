#!/usr/bin/env python

"""TeachableHub APIs for Python
See:
https://github.com/teachablehub/python-sdk
"""
from setuptools import setup, find_packages
from teachablehub import version as pkg_version
from codecs import open

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name='teachablehub',
    version=pkg_version,
    description='TeachableHub Machine Learning Platform SDK. Deployments, Predictions, and Management.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/teachablehub/python-sdk',
    author='Marian Ignev',
    author_email='dev@teachablehub.com',
    packages=find_packages(
        exclude=['test', 'build', 'dist', 'venv', 'teachablehub.egg-info']),
    keywords='deep learning deep_learning machine machine_learning natural language processing computer vision',
    install_requires=[
        'uplink==0.9.3',
        'th-sklearn-json',
        'numpy',
    ],
    python_requires='>=3.4',
)
