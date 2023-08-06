#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=line-too-long,missing-module-docstring,exec-used

import setuptools


with open("README.md", 'r', encoding='utf-8') as fh:
    long_description = fh.read()


setuptools.setup(
    name='lisainstrument',
    use_scm_version=True,
    author='Jean-Baptiste Bayle',
    author_email='j2b.bayle@gmail.com',
    description='LISA Instrument simulates instrumental noises, propagates laser beams, generates measurements and the on-board processing to deliver simulated telemetry data.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.in2p3.fr/lisa-simulation/instrument",
    license='BSD-3-Clause',
    packages=setuptools.find_packages(),
    install_requires=[
        'h5py',
        'numpy',
        'scipy',
        'matplotlib',
        'lisaconstants',
        'packaging',
        'importlib_metadata',
    ],
    setup_requires=['setuptools_scm'],
    tests_require=['pytest'],
    python_requires='>=3.7',
)
