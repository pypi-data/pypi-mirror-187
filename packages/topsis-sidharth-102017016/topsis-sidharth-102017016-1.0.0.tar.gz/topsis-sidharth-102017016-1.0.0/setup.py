from setuptools import setup, find_packages
import codecs
import os



VERSION = '1.0.0'
DESCRIPTION = 'Topsis package'
LONG_DESCRIPTION = 'A package that applies topsis to the given data and outputs a csv file.'

# Setting up
setup(
    name="topsis-sidharth-102017016",
    version=VERSION,
    author="Sidharth Bahl",
    author_email="<bahlsidharth@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pandas','numpy'],
    keywords=['python', 'topsis', 'data science', 'data analysis'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)