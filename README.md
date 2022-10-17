# dicomgenerator


[![CI](https://github.com/sjoerdk/dicomgenerator/actions/workflows/build.yml/badge.svg?branch=master)](https://github.com/sjoerdk/dicomgenerator/actions/workflows/build.yml?query=branch%3Amaster)
[![PyPI](https://img.shields.io/pypi/v/dicomgenerator)](https://pypi.org/project/dicomgenerator/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dicomgenerator)](https://pypi.org/project/dicomgenerator/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

Generate pydicom datasets and data elements for use in testing.

* Free software: MIT license
* Status: Alpha. Tests run but there are loose ends

Features
--------
* Extends [factory-boy](https://factoryboy.readthedocs.io) factories to produce [pydicom](https://github.com/pydicom/pydicom) Datasets and DicomElements 
* Generate valid DICOM values for person name, time, date, and UID
* Create json-based editable templates from any dicom file
* quick_dataset(): single-line pydicom dataset init

## Installation


Install with pip::

    pip install dicomgenerator


## Usage
### Quick dataset
I have found this quite useful in testing:

```python
    from dicomgenerator.generators import quick_dataset
    ds = quick_dataset(PatientName='Jane', StudyDescription='Test')

    # >>> ds.PatientName -> 'Jane'     
    # >>> ds.StudyDescription -> 'Test'
```


### Generating a dataset
Generate a realistic CT dataset

```python 
    from dicomgenerator.factory import CTDatasetFactory

    # Generate from template
    >>> CTDatasetFactory().PatientName -> 'van Haarlem^Anouk'  #  generated random name
    >>> CTDatasetFactory().PatientName -> 'Loreal^Casper'      #  generated random name

    # Overwrite arbitrary DICOM elements
    ds.CTDatasetFactory(PatientSex='M', PatientName='Smith^Harry')
    >>> ds.PatientName -> 'Smith^Harry'
    >>> ds.PatientSex  -> 'M'

    # generated UIDs and dates are valid DICOM
    >>> CTDatasetFactory().StudyTime        -> '130624.929'
    >>> CTDatasetFactory().StudyDate        -> '20110508'
    >>> CTDatasetFactory().StudyInstanceUID -> '1.2.826.0.1.3680'
```


## Generating a data element

```python
    # import
    from dicomgenerator.factory import DataElementFactory

    # Creating a DICOM data element by name will give a realistic value and correct VR
    >>> DataElementFactory(tag='PatientName').value -> "van Ooyen^Fiene"
    >>> DataElementFactory(tag='PatientName').VR -> 'PN'

    # You can also give DICOM tags as hex
    >>> DataElementFactory(tag=0x00100010).value -> "Weil^Jack"

    # Dates, times and UIDs all work.
    >>> DataElementFactory(tag="AcquisitionTime").value   -> '184146.928'
    >>> DataElementFactory(tag="PatientBirthDate").value  -> '20120511'
    >>> DataElementFactory(tag="SeriesInstanceUID").value -> '1.2.826.0.1.3680'
```

### In reproducible tests
You can set the random seed in [factory-boy](https://factoryboy.readthedocs.io) like this:

```python
    from factory import random

    def test_one:
        """The random patient name in this test will always be the same"""
        random.reseed_random('any string you want')
        assert element = DataElementFactory(tag='PatientName').value == "van Ooyen^Fiene"
```

### Command Line Interface
You can convert a DICOM file to AnnotatedDataset via the commandline. by default this will write an annotated dataset to the same folder, appending`_template.json`

```
$ dicomgen convert to-json /tmp/dicom_file
$ ls
dicom_file  dicom_file_template.json
```

For options, use
```
$ dicomgen convert to-json --help
```


## Credits

This package was originally created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) project template.
 
