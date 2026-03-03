from copy import deepcopy
from io import BytesIO

import pytest
from pydicom import Dataset, dcmread

from dicomgenerator.generators import quick_dataset
from dicomgenerator.pixeldata import Block, add_blocks, draw_noise, add_pixel_data_2d


def simulate_read_from_disk(ds: Dataset) -> Dataset:
    """Save and then read from disk again. This catches many subtle issues

    Warning
    -------
    This sets dummy values for MediaStorageSOPClassUID and other elements needed for
    saving to disk. To be improved.
    """
    dicom_file = BytesIO()
    ds.file_meta.MediaStorageSOPClassUID = "1.2.3"
    ds.file_meta.MediaStorageSOPInstanceUID = "4.5.6"
    ds.save_as(dicom_file, enforce_file_format=True)
    dicom_file.seek(0)
    return dcmread(dicom_file)


def test_write_pixel_dataset():
    # create a test file with noise
    ds = quick_dataset(PatientID="TestPatient", Modality="CT")
    pixel_values = draw_noise(201, 301, "uint8")
    ds = add_pixel_data_2d(dataset=ds, pixel_array=pixel_values, dtype="uint8")

    # create a copy, and black out two blocks
    ds2 = deepcopy(ds)
    blocks = [Block(10, 10, 50, 200), Block(100, 100, 40, 40)]
    ds2 = add_blocks(ds2, blocks, value=0)

    # write to file to catch some persistence errors
    ds = simulate_read_from_disk(ds)
    ds2 = simulate_read_from_disk(ds2)

    # check whether blocks are really written
    # ds2.pixel_array[10:15, 9:20] == 0
    for block in blocks:
        assert not ds2.pixel_array[block.as_2d_slice()].any()  # no non-zero values
        assert ds.pixel_array[block.as_2d_slice()].any()  # should have non-zero values

    # for debug, use this:
    # plt.imshow(ds.pixel_array)
    # plt.show()


def test_write_blocks_exceptions():
    # create a test file with noise
    ds = quick_dataset(PatientID="TestPatient", Modality="CT")
    pixel_values = draw_noise(201, 301, "uint8")
    ds = add_pixel_data_2d(dataset=ds, pixel_array=pixel_values, dtype="uint8")

    with pytest.raises(OverflowError):
        # Setting an impossible value will raise exception
        add_blocks(ds, [Block(10, 10, 50, 200)], value=1000)

    # adding blocks that extend beyond the image is weird. Probably a user error. Raise
    with pytest.raises(ValueError):
        add_blocks(ds, [Block(-2, 10, 50, 50)], value=0)

    with pytest.raises(ValueError):
        add_blocks(ds, [Block(10, -2, 50, 50)], value=0)

    with pytest.raises(ValueError):
        add_blocks(ds, [Block(10, 20, 500, 50)], value=0)
