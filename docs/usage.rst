=====
Usage
=====

Generating a pydicom dataset::

    from dicomgenerator.factory import CTDatasetFactory

    # Generate from template
    >>> CTDatasetFactory().PatientName = 'van Haarlem^Anouk'  #  generated random name
    >>> CTDatasetFactory().PatientName = 'Loreal^Casper'      #  generated random name

    # Overwrite arbitrary DICOM elements
    ds.CTDatasetFactory(PatientSex='M', PatientName='Smith^Harry')
    >>> ds.PatientName = 'Smith^Harry'
    >>> ds.PatientSex  = 'M'

    # generated UIDs and dates are valid DICOM
    >>> CTDatasetFactory().StudyTime        = '130624.929'
    >>> CTDatasetFactory().StudyDate        = '20110508'
    >>> CTDatasetFactory().StudyInstanceUID = '1.2.826.0.1.3680'



Generating a pydicom data element::

    from dicomgenerator.factory import DataElementFactory

    # Creating a DICOM data element by name will give a realistic value and correct VR
    >>> DataElementFactory(tag='PatientName').value  = "van Ooyen^Fiene"
    >>> DataElementFactory(tag='PatientName').VR == 'PN'

    # You can also give DICOM tags as hex
    >>> DataElementFactory(tag=0x00100010).value = "Weil^Jack"

    # Dates, times and UIDs all work.
    >>> DataElementFactory(tag="AcquisitionTime").value = '184146.928'
    >>> DataElementFactory(tag="PatientBirthDate").value = '20120511'
    >>> DataElementFactory(tag="SeriesInstanceUID").value = '1.2.826.0.1.3680'



In reproducible tests
=====================

You can set the random seed like this::

    from factory import random

    def test_one:
        """The random patient name in this test will always be the same"""
        random.reseed_random('any string you want')
        assert element = DataElementFactory(tag='PatientName').value == "van Ooyen^Fiene"


