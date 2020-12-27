#!/usr/bin/env python3

"""setuptools/wheel/PyPI version of the aeidon package."""

import shutil

from setup import get_aeidon_version
from setuptools import find_packages
from setuptools import setup

# Copy data files to the aeidon package, so they can be included.
shutil.copytree("data/headers", "aeidon/data/headers")
shutil.copytree("data/patterns", "aeidon/data/patterns")

setup(
    name="aeidon",
    version=get_aeidon_version(),
    author="Osmo Salomaa",
    author_email="otsaloma@iki.fi",
    description="Reading, writing and manipulating text-based subtitle files",
    long_description=open("README.aeidon.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/otsaloma/gaupol",
    license="GPL",
    packages=find_packages(exclude=["gaupol*", "*.test"]),
    package_data={"aeidon": ["data/*/*"]},
    python_requires=">=3.2.0",
    install_requires=["chardet>=2.2.1"],
)

shutil.rmtree("aeidon/data")
