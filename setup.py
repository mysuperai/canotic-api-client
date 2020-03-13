# coding: utf-8


from setuptools import setup, find_packages

NAME = "canotic_api_client"
VERSION = "0.0.1"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "boto3==1.9.188",
    "requests==2.22.0",
    "Click==7.0",
    "warrant==0.6.1"
]

setup(
    name=NAME,
    version=VERSION,
    description="Canotic API",
    author_email="",
    url="https://canotic.com/",
    keywords=["Canotic API"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description="""\
    Canotic App Store API  
    """,
    entry_points={
        'console_scripts': [
            'canotic-api-cli=canotic.cli:main',
        ],
    },
)
