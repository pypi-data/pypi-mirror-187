from setuptools import setup, find_packages
import pandas as pd
import numpy as np
import os
import sys
VERSION = '0.0.1'
DESCRIPTION = 'A Package for Topsis'
LONG_DESCRIPTION = 'A Package for Topsis for Multiple Criteria Decision Making using Topsis where CSV file is passed using commandline'

# Setting up
setup(
    name="Topsis-AbhijotSingh-102003164",
    version=VERSION,
    author="Abhijot Singh",
    author_email="<asingh29_be20@thapar.edu>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    install_requires=['numpy', 'pandas'],
    keywords=['python', 'Topsis', 'MultipleDecision', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
