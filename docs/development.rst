===========
Development
===========

Extending dicomgenerator
========================

To add a template based on a DICOM file:

* Fork the dicomgenerator repo on github
* See examples -> collect_data_from_existing_dicom.py
* Add class YourTemplate(DatasetFactory) to factory.py
* Add minimal tests
* Make a pull request
