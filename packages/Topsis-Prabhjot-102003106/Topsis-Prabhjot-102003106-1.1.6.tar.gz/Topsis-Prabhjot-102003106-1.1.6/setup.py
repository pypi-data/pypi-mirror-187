from setuptools import setup
import pathlib
import codecs
import os

HERE = pathlib.Path(__file__).parent
VERSION = '1.1.6'
DESCRIPTION = 'Topsis Calculation Package'
LONG_DESCRIPTION = README = (HERE / "README.md").read_text(encoding="UTF-8")
L_ICENCE_NEW = LICENCE = (HERE / "LICENCE.txt").read_text(encoding="UTF-8")

# Setting up
setup(
    name="Topsis-Prabhjot-102003106",
    version=VERSION,
    author="Prabhjot Singh Bhatia",
    author_email="<prabh3876@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    licence=L_ICENCE_NEW,
    packages=["Topsis"],
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