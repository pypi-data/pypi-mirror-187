from setuptools import setup, find_packages


VERSION = '0.0.4'

# Setting up
setup(

    name="102003712",
    version=VERSION,
    author="Garima Mittal",
    author_email="gmittal1_be20@thapar.edu",
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'video', 'stream',
              'video stream', 'camera stream', 'sockets'],
    entry_points={
        'console_scripts': [
            'topsis=topsisLibrary.topsis:main'
        ]
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.5',
)
