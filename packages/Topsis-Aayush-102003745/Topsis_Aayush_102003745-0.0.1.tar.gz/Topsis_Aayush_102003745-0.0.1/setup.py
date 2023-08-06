from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Streaming video data via networks'
LONG_DESCRIPTION = ''

# Setting up
setup(
    name="Topsis_Aayush_102003745",
    version=VERSION,
    author="Aayush Asrey",
    author_email="aasrey_be20@thapar.edu",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['pandas'],
    keywords=[],
    classifiers=[
    ]
)