from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.0.1'
DESCRIPTION = 'Topsis Algorithm'
LONG_DESCRIPTION = 'Topsis package to calculate topsis score and rank when there are multiple critera involved'

# Setting up
setup(
    name="Topsis-Rishu-102003725",
    version=VERSION,
    author="Rishu Anand",
    author_email="<anand.rishu310@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pandas', 'numpy'],
    keywords=['python', 'topsis', 'ranking algorithm', 'multiple criteria'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)