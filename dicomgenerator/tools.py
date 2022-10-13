"""Functions and classes for turning existing DICOM files into editable datasets
and templates
"""
import pydicom
from pathlib import Path

import numpy as np

from PIL import Image

from dicomgenerator.annotation import AnnotatedDataset
from dicomgenerator.resources import RESOURCE_PATH


def dataset_to_json(dataset, replace_image_data=True, description="Converted"):
    """Turn dataset into a template. Replaces image data with tiny dummy image
    by default
    """
    if replace_image_data:
        dataset = replace_pixel_data(
            dataset, image_path=RESOURCE_PATH / "skeleton_tiny.jpg"
        )

    return AnnotatedDataset(dataset=dataset, description=description)


def to_annotated_dataset(input_path, output_path=None, description="Converted"):
    """Reads dicom file at path and convert to annotated dataset

    Parameters
    ----------
    input_path: str:
        read dicom file here

    output_path: str, optional
        write annotated set to this path. If not given will write to <input_path>.json

    description: str, optional
        human-readable description of this dataset

    Returns
    -------
    The path that was written to
    """
    input_path = Path(input_path)
    if output_path:
        output_path = Path(output_path)
    else:
        output_path = input_path.parent / (input_path.stem + "_template.json")

    dataset = pydicom.dcmread(input_path)
    with open(output_path, "w") as f_out:
        dataset_to_json(dataset, description=description).save(f_out)
    return output_path


def replace_pixel_data(dataset, image_path):
    """Replace the DICOM PixelData tag with the data from image_path

    Parameters
    ----------
    dataset: pydicom.dataset.Dataset
    image_path: pathlike to rgb image readable with pillow

    Returns
    -------
    pydicom.dataset.Dataset
        With replaced PixelData and Columns and Rows changed to match

    """
    im = Image.open(image_path)
    pixel_values = list(im.getdata())
    # convert image into numpy ndarray. use only R channel from RGB as this is
    # a greyscale image
    pix_np = np.array([x[0] for x in pixel_values])
    w, h = im.size  # Set dimensions
    pix_np.shape = (h, w)
    pix_np = rescale(pix_np, min=-2048, max=1000)  # make values CT-like
    dataset.PixelData = pix_np.astype(
        np.int16
    ).tostring()  # Not sure whether this can be other than int16.
    dataset.Rows, dataset.Columns = pix_np.shape
    return dataset


def rescale(ndarray, min, max):
    """Rescale values of ndarray linearly so min of ndarray is min, max is max

    Parameters
    ----------
    ndarray: numpy nd array
    min: int
    max: int

    Returns
    -------
    numpy ndarray

    """

    old_max = ndarray.max()
    old_min = ndarray.min()
    old_range = old_max - old_min
    old_dtype = ndarray.dtype
    new_range = max - min
    range_scale = new_range / old_range

    ndarray = ndarray.astype(float)
    ndarray -= old_min  # translate to make based on 0
    ndarray *= range_scale  # scale to make range same size
    ndarray += min  # translate back to make old min fall on (new) min

    return ndarray.astype(old_dtype)
