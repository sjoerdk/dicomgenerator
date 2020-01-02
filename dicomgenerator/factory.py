"""Generate pydicom datasets to look like different types of DICOM

"""
import factory
import pydicom


class DatasetFactory(factory.Factory):
    class Meta:
        model = pydicom.dataset.Dataset

