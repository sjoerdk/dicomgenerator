"""
Reads in existing DICOM files and tries to record as many crappy details as possible
Saves this so it can be used to generate DICOM later
"""
from pydicom.dataset import Dataset


def to_json(dataset):
    """Converts pydicom dataset to JSON.

    Wraps more powerful pydicom functions with convenience wrapper

    Parameters
    ----------
    dataset: pydicom.dataset.Dataset
        Input data. Usually read with pydicom.dcmread

    Returns
    -------
    str
        Json encoded representation of the metadata of this datatset. Includes
        private tags.

    """
    dataset.decode()

    def just_decode_handler(input):
        return {'vr': input.VR,
                'InlineBinary': input.value.decode()}

    megabyte = 1024 * 1024
    return dataset.to_json(bulk_data_element_handler=just_decode_handler,
                           bulk_data_threshold=megabyte * 3)


