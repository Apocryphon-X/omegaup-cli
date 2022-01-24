# -*- coding: utf-8 -*-
"""setup.py: setuptools control."""

from setuptools import setup
import subprocess

with open("README.md", "r", encoding="utf-8") as target_file:
    long_description = target_file.read()

with open("requirements.txt", "r") as target_file:
    install_requires = target_file.read().strip().split("\n")

# actual_version = subprocess.check_output(
#    ["/usr/bin/git", "describe", "--tags"], universal_newlines=True
# )

setup(
    name="omegaup_cli",
    version="0.1.0a5",
    python_requires=">=3.8",
    long_description=long_description,
    long_description_content_type="text/markdown",
    description="CLI for OmegaUp users.",
    license="MIT",
    author="Dante Mendoza Leyva (Apocryphon-X)",
    author_email="apocryphon.x.contact@gmail.com",
    # url="https://github.com/Apocryphon-X/omegaup-cli",
    packages=["ucli"],
    entry_points={"console_scripts": ["ucli = ucli.cli:main"]},
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
