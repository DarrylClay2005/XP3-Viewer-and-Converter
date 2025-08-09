#!/usr/bin/env python3
"""
Setup script for XP3 Viewer and Converter
"""

from setuptools import setup, find_packages
import os

# Read README file for long description
def read_readme():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()

# Read requirements
def read_requirements():
    with open('requirements.txt', 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="xp3-viewer-converter",
    version="1.0.2",
    author="XP3 Viewer Team",
    description="A GUI application for viewing and converting XP3 archive files",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/XP3-Viewer-and-Converter",
    packages=find_packages(),
    py_modules=['xp3_viewer_converter'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Graphics :: Viewers",
        "Topic :: System :: Archiving",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    entry_points={
        'console_scripts': [
            'xp3-viewer=xp3_viewer_converter:main',
        ],
        'gui_scripts': [
            'xp3-viewer-gui=xp3_viewer_converter:main',
        ],
    },
    include_package_data=True,
    keywords="xp3 archive viewer converter kirikiri visual novel",
)
