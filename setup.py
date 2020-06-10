#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Pillow==6.2.2', 'numpy==1.18.0',
                'pydicom>2.0',
                'matplotlib==3.1.2', 'factory-boy==2.12.0']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3',]

setup(
    author="Sjoerd Kerkstra",
    author_email='sjoerd.kerkstra@radboudumc.nl',
    python_requires='~=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Create DICOM images for use in testing. Based on pydicom",
    entry_points={
        'console_scripts': [
            'dicomgenerator=dicomgenerator.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='dicomgenerator',
    name='dicomgenerator',
    packages=find_packages(include=['dicomgenerator']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/sjoerdk/dicomgenerator',
    version='0.2.0',
    zip_safe=False,
)