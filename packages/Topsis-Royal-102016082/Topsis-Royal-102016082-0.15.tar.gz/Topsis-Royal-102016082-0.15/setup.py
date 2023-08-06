from setuptools import setup
import codecs
import os

VERSION = '0.15'
DESCRIPTION = 'Topsis Package'

# Setting up
setup(
    name="Topsis-Royal-102016082",
    version=VERSION,
    url="https://github.com/RGarg2002/Assignment1_topsis/tree/master/Topsis-Royal-102016082",
    author="Royal Garg",
    author_email="<royalgarg36@gmail.com>",
    description=DESCRIPTION,
    license="MIT",
    packages=["topsis_assignment"],
    install_requires=[],
    
    entry_points={
        "console_scripts": [
            "topsis=topsis_assignment.__main__:main",
        ]
    },
    keywords=['python', 'topsis', 'machine learning', 'assignment'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)