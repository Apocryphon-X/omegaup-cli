"""setup.py: setuptools control."""

from setuptools import setup

actual_version = "0.1.0a0"

setup(
    name = "omegaup_cli",
    version = actual_version,
    python_requires = ">=3.8",

    description = "CLI for OmegaUp users.",
    license = "MIT",
    
    author = "Dante Mendoza Leyva (Apocryphon-X)",
    author_email = "apocryphon.x.contact@gmail.com",
    url = "https://github.com/Apocryphon-X/omegaup-cli",
    
    packages = ["src"],
    entry_points = {
        "console_scripts": ["ucl = src.cli:main"]
    },
    install_requires = [
        "requests",
        "stdiomask",
        "click",
        "blessed>=1.18.0",
        "omegaup>=1.3.0"
    ],
    
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
