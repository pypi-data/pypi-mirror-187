from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Premade Cool Python Codes'

# Setting up
setup(
    name="useit",
    version=VERSION,
    author="Aarush Mehta",
    author_email="<aarush07codec@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['webbrowser', 'pynotifier', 'pyautogui', 'psutil', 'pywhatkit', 'wikipedia'],
    keywords=['python', 'python3', 'autocode', 'premade code', 'code', 'programming'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
