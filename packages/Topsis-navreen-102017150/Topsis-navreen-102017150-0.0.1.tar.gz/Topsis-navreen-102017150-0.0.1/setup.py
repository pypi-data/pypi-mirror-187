import os
from setuptools import setup

NAME = "Topsis-navreen-102017150"
VERSION = "0.0.1"
DESCRIPTION = "A python package for topsis score computation."
AUTHOR = "Navreen Waraich"
AUTHOR_EMAIL = "navreenwaraich@gmail.com"
PACKAGES_PRESENT = ['Topsis']
PACKAGES_NEED = ['pandas','numpy']

def read_file(name):
    path = os.getcwd()
    return open(f"{path}\{name}").read()

setup(
    name = NAME,
    version = VERSION,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    description = DESCRIPTION,
    packages = PACKAGES_PRESENT,
    install_requires = PACKAGES_NEED,
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    license = read_file('LICENSE.md')
)
