from setuptools import setup, find_packages
import codecs
import os

 
VERSION = '0.0.2 '
DESCRIPTION = 'A Topsis Package' 

# Setting up
setup(
    name="102003712",
    version=VERSION,
    author="Garima Mittal",
    author_email="<gmittal1_be20@thapar.edu>",
    description=DESCRIPTION,
    
    packages=find_packages(),
    install_requires=[ ],
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)