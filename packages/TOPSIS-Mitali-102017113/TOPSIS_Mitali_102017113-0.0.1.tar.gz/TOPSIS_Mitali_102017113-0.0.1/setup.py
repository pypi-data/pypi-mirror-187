from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'My Topsis package'



setup(
    name="TOPSIS_Mitali_102017113",
    version=VERSION,
    author="Mitali Jain",
    author_email="<mjain2_be20@thapar.edu>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy', 'pandas', 'sys'],
    keywords=['python', 'topsis', 'machinelearning', 'datascience'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)