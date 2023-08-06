from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Libelium One message decode'
LONG_DESCRIPTION = 'A package that allows to convert from' +\
    'hexadecimal strings to values read from sensors.'

# Setting up
setup(
    name="onedecoding",
    version=VERSION,
    author="Noel Gomariz",
    author_email="noel.gomaku@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    install_requires=[],
    packages=find_packages(),
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)