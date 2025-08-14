#!/usr/bin/env python3
"""
Setup script for Seq80x25
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="seq80x25",
    version="1.0.0",
    author="frangedev",
    author_email="",
    description="A retro-inspired, terminal-based music sequencer",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/frangedev/seq80x25",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Multimedia :: Sound/Audio :: MIDI",
        "Topic :: Multimedia :: Sound/Audio :: Editors",
        "Topic :: Terminals",
        "Topic :: Artistic Software",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "seq80x25=seq80x25:main",
        ],
    },
    include_package_data=True,
    package_data={
        "seq80x25": ["*.css", "*.txt", "*.png"],
    },
    keywords="music, sequencer, terminal, retro, chiptune, pygame, textual",
    project_urls={
        "Bug Reports": "https://github.com/frangedev/seq80x25/issues",
        "Source": "https://github.com/frangedev/seq80x25",
        "Documentation": "https://github.com/frangedev/seq80x25#readme",
    },
)
