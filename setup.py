"""setup.py: setuptools control."""

from setuptools import setup, find_packages

long_descr = """
A Simple CLI for OmegaUp.
Features:
- Make Submits
- Manage Contests
- Manage Problems
- And more!
"""
version = "0.0.5a"

setup(
    name="omegaup_cli",
    packages=["omegaup"],
    entry_points={
        "console_scripts": ["ucl = omegaup.cli:main"]
    },
    version=version,
    description="CLI for OmegaUp users",
    long_description=long_descr,
    author="Dante Mendoza Leyva (Apocryphon-X)",
    author_email="apocryphon.x.contact@gmail.com",
    license="MIT",
    url="https://github.com/Apocryphon-X/omegaup-cli",
    install_requires=[
        "requests",
        "termcolor",
        "stdiomask"
    ],
  # package_data={
  #     "omegaup": ["models/*"]
  # },
    include_package_data = True,
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: Early Alpha",
        "Environment :: Console",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
