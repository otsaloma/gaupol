#!/usr/bin/env python3

"""
PyPI version of the aeidon package.

This script is only for building a package to upload to PyPI!
If building separate aeidon and gaupol packages for a distro,
please use the main setup.py as explained in README.aeidon.md.
"""

import shutil

from setup import get_aeidon_version
from setuptools import find_packages
from setuptools import setup

# Copy data files to the aeidon package, so they can be included.
shutil.copytree("data/headers", "aeidon/data/headers")
shutil.copytree("data/patterns", "aeidon/data/patterns")

with open("README.aeidon.md", "r") as f:
    long_description = f.read()

setup(
    name="aeidon",
    version=get_aeidon_version(),
    author="Osmo Salomaa",
    author_email="otsaloma@iki.fi",
    description="Reading, writing and manipulating text-based subtitle files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/otsaloma/gaupol",
    license="GPL",
    packages=find_packages(exclude=["gaupol*", "*.test"]),
    package_data={"aeidon": ["data/*/*"]},
    python_requires=">=3.5.0",
    install_requires=["charset-normalizer>2.0"],
)

shutil.rmtree("aeidon/data")
