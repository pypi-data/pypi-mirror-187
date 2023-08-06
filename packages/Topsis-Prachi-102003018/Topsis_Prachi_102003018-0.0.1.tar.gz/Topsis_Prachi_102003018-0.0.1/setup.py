from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'command line tool for calculating topsis score'
LONG_DESCRIPTION = 'command line tool for calculating topsis score'

# Setting up
setup(
    name="Topsis_Prachi_102003018",
    version=VERSION,
    author="Prachi Gupta",
    author_email="pr.gupta059@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['logging', 'pandas'],
    keywords=['topsis'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)