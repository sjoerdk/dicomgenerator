==============
dicomgenerator
==============



.. image:: https://github.com/sjoerdk/dicomgenerator/workflows/build/badge.svg
        :target: https://github.com/sjoerdk/dicomgenerator/actions?query=workflow%3Abuild
        :alt: Build Status

.. image:: https://img.shields.io/pypi/v/dicomgenerator.svg
    :target: https://pypi.python.org/pypi/dicomgenerator


Generate pydicom datasets and data elements for use in testing.


* Free software: MIT license
* Documentation: https://dicomgenerator.readthedocs.io.


Features
--------

* Generates random valid DICOM values for person name, time, date, and UID
* Generates (templated) pydicom Datasets and DicomElements
* leverages Factory Boy to generate arbitrary permutations of any template
* Create templates from any DICOM file
* Optionally replace image data with dummy data

Installation
------------

Install with pip::

    pip install dicomgenerator


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
