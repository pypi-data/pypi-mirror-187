from setuptools import setup
import pathlib
import codecs
import os

HERE = pathlib.Path(__file__).parent
VERSION = '1.1.10'
DESCRIPTION = 'Topsis Package'
LONG_DESCRIPTION = README = (HERE / "README.md").read_text()
L_ICENSE = LICENSE = (HERE / "LICENSE.txt").read_text()

# Setting up
setup(
    name="Deepak_102003483",
    version=VERSION,
    author="Deepak Aggarwal",
    author_email="<daggarwal2_be20@thapar.edu>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    license = L_ICENSE,
    packages=['Topsis'],
    install_requires=['pandas', 'numpy', 'detect_delimiter', 'scipy'],
    keywords=['python', 'topsis', 'mcdm'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    entry_points={
        'console_scripts': [
            'cursive = cursive.tools.cmd:cursive_command',
        ],
    }
)