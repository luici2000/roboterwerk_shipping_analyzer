#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Setup-Skript für Roboterwerk Shipping Analyzer."""

from setuptools import setup, find_packages
from pathlib import Path

# README einlesen
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name='roboterwerk-shipping-analyzer',
    version='1.0.0',
    author='Roboterwerk GmbH',
    author_email='info@roboterwerk.de',
    description='Analysiert Lieferschein-PDFs der Roboterwerk GmbH',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/roboterwerk_shipping_analyzer',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Office/Business',
        'Natural Language :: German',
    ],
    python_requires='>=3.8',
    install_requires=[
        'PyMuPDF>=1.23.0',
        'openpyxl>=3.1.0',
    ],
    entry_points={
        'console_scripts': [
            'roboterwerk-analyzer=roboterwerk_analyzer.__main__:main',
        ],
    },
    include_package_data=True,
    keywords='pdf, lieferschein, analyse, roboterwerk, drohnen, excel, csv',
)
