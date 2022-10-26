from pathlib import Path

from pydicom.dataset import Dataset
from pydicom.uid import CTImageStorage, ExplicitVRLittleEndian


def export(dataset: Dataset, path: Path, force=True):
    """Save dataset to path, forcing default and dummy values to save

    Parameters
    ----------
    dataset:
        The dataset to save
    path:
        The path to save to
    force: Bool, optional
        If true, fill in/ make up missing DICOM values to make this dataset save.
        See notes below. Defaults to True

    Notes
    -----
    Force saving is meant mainly for test cases where you do not care about DICOM
    intricacies, you just want to write DICOM to disk.
    Forcing means selecting some common settings for encoding, endedness, even
    class of image (CT by default).


    """
    if force:
        force_make_savable(dataset).save_as(str(path), write_like_original=False)
    else:
        dataset.save_as(str(path), write_like_original=True)


def force_make_savable(dataset):
    """Set values in dataset that will make it save. This ignores many DICOM
    intricacies and just picks some common values for required fields that might
    not be completely appropriate for the given dataset. If you do not care too much
    and just want to test some DICOM, this is for you. Go for it.
    """
    # set most common options
    dataset.is_little_endian = True
    dataset.is_implicit_VR = False

    # ensure meta information that is needed for persisting to disk
    if not hasattr(dataset, "file_meta"):
        dataset.ensure_file_meta()
        dataset.file_meta.MediaStorageSOPClassUID = CTImageStorage
        dataset.file_meta.MediaStorageSOPInstanceUID = dataset.SOPInstanceUID
        dataset.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

    return dataset
