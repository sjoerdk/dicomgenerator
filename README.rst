==============
dicomgenerator
==============


.. image:: https://github.com/DIAGNijmegen/dicomgenerator/workflows/build/badge.svg
        :target: https://github.com/sjoerdk/dicomgenerator/actions?query=workflow%3Abuild
        :alt: Build Status


Create DICOM images for use in testing. Uses pydicom.


* Free software: MIT license
* Documentation: https://dicomgenerator.readthedocs.io.


Features
--------

* Create templates from any DICOM file
* Optionally replace image data with dummy data
* Use pytest to generate arbitrary permutations of any template
* Includes pytest provider for generating valid DICOM values for person name, time, date, and UID

Installation
------------

Currently using dev version of pydicom. To install use::

   pip install git+ssh://git@github.com/pydicom/pydicom.git


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
