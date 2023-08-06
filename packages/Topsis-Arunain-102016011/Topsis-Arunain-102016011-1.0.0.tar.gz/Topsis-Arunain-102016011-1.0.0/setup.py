import os
from setuptools import setup

NAME = "Topsis-Arunain-102016011"
VERSION = "1.0.0"
DESCRIPTION = "A package for topsis score generation."
AUTHOR = "Arunain"
AUTHOR_EMAIL = "aarunain_be20@thapar.edu"
PACKAGES_PRESENT = ['src']
PACKAGES_NEED = ['pandas','numpy']
PACKAGE_DIR={'':'src'}

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