from setuptools import setup, find_packages
import codecs
import os


here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.16'
DESCRIPTION = 'A BDM ENG!'
LONG_DESCRIPTION = 'A library for managing sales leads'

setup(
    name='BDevManager',
    version=VERSION,
    install_requires=[],
    author='blackfox',
    author_email='andrew@blackfoxstudios.org',
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    url='https://github.com/BlackFoxgamingstudio/andrew_bdm.git',
)
