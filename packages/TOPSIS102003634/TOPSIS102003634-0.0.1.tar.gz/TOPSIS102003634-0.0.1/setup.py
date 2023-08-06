from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Package implementing TOPSIS.'


# Setting up
setup(
    name="TOPSIS102003634",
    version=VERSION,
    author="Falguni Sharma",
    author_email="<fsharma_be20@thapar.edu>",
    description=DESCRIPTION,
    
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'TOPSIS'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)