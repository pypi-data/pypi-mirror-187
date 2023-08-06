from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.0.1'
DESCRIPTION = 'Idit your csv files'
LONG_DESCRIPTION = 'A package that allows to edit csv file you can creat and write in it and remove it.'

# Setting up
setup(
    name="csvedit",
    version=VERSION,
    author="Boudaoudkamal (Florian Dedov)",
    author_email="<boudaoudkamel75@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pandas'],
    keywords=['write', 'files', 'csv', 'panas', 'camera stream', 'creat'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
