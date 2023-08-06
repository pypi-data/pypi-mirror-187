#!/usr/bin/env python

"""Setup script for the package."""

import setuptools
import sys


MINIMUM_PYTHON_VERSION = 3, 7


def check_python_version():
    """Exit when the Python version is too low."""
    if sys.version_info < MINIMUM_PYTHON_VERSION:
        sys.exit("Python {}.{}+ is required.".format(*MINIMUM_PYTHON_VERSION))


check_python_version()

setuptools.setup(
    description="Binary Star Package for Ball State University's Astronomy Research Group",
    url='https://github.com/kjkoeller/Binary_Star_Research_Package',
    author='Kyle Koeller',

    packages=setuptools.find_packages(),

    entry_points={'console_scripts': []},

    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=[
        'astropy>=5.1.1',
        'astroquery>=0.4.6',
        'ccdproc>=2.4.0',
        'matplotlib>=3.3.1',
        'numpy>=1.19.1',
        'pandas>=1.1.0',
        'PyAstronomy>=0.18.0',
        'scipy>=1.5.2',
        'statsmodels>=0.13.5',
        'tqdm>=4.64.1',
        'numba>=0.56.3'
    ]
)
