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
    "botocore==1.12.188",
    "certifi==2019.6.16",
    "chardet==3.0.4",
    "Click==7.0",
    "docutils==0.14",
    "ecdsa==0.13.3",
    "envs==1.3",
    "future==0.17.1",
    "idna==2.8",
    "jmespath==0.9.4",
    "pycryptodome==3.6.6",
    "python-dateutil==2.8.0",
    "python-jose-cryptodome==1.3.2",
    "requests==2.22.0",
    "s3transfer==0.2.1",
    "six==1.12.0",
    "urllib3==1.25.3",
    "warrant==0.6.1"

]

setup(
    name=NAME,
    version=VERSION,
    description="Canotic API",
    author_email="",
    url="canotic.com",
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
