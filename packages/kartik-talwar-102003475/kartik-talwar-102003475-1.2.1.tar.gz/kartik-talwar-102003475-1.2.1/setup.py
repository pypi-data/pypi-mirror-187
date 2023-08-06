from setuptools import setup
import pathlib
import codecs
import os

HERE = pathlib.Path(__file__).parent
VERSION = '1.2.1'
DESCRIPTION = 'Topsis Calculation Package'
LONG_DESCRIPTION = README = (HERE / "README.md").read_text()

# Setting up
setup(
    name="kartik-talwar-102003475",
    version=VERSION,
    author="Kartik Talwar",
    author_email="<ktalwar_be20@thapar.edu>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=['topsis'],
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