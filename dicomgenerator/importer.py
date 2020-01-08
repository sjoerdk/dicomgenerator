"""
Reads in existing DICOM files and tries to record as many details as possible
Saves this so it can be used to generate DICOM later
"""
import json
import uuid
from pathlib import Path

import numpy as np

from PIL import Image
from pydicom.dataset import Dataset

from dicomgenerator.resources import RESOURCE_PATH


class Template:
    """A couple of files describing a dicom template. Makes is easy to save a
    human readable description together with the template

    """

    def __init__(self, template=None, description=None):
        """

        Parameters
        ----------
        template: pydicom.dataset.Dataset
            Dicom dataset
        description: str
            Human readable description of this template

        """
        self.template = template
        self.description = description

    def save(self, output_path):
        """Save template to output path. Save description <output_path>.txt

        Parameters
        ----------
        output_path: Path

        """
        with open(output_path, 'w') as f:
            f.write(to_json(self.template))
        if self.description:
            with open(self.get_description_path(output_path), 'w') as f:
                f.write(self.description)

    @staticmethod
    def get_description_path(template_path):
        return Path(template_path.parent / (str(template_path.stem) + ".txt"))

    @classmethod
    def load(cls, template_path):
        """
        Parameters
        ----------
        template_path: Path
            Full path to json path

        Returns
        -------
        Template
            Read from template path

        """
        description_path = cls.get_description_path(template_path)

        if description_path.exists():
            with open(description_path, 'r') as f:
                description = f.readlines()
        else:
            description = None

        with open(template_path, 'r') as f:
            template = Dataset.from_json(json.load(f))
        return cls(template=template, description=description)

    def get_description(self):
        """Get the description for this template

        Returns
        -------
        str:
            Contents of description file
        None:
            If file does not exist

        """
        if self.description_path.exists():
            with open(self.description_path + ".json", 'r') as f:
                return f.readlines()
        else:
            return None

    def get_dicom_template(self):
        """

        Returns
        -------
        parsed json structure

        """
        with open(self.folder_path / self.file_name + ".json", 'r') as f:
            return json.read(f)


def save_as_template(dataset, description=None, output_path=None):
    """Saves the given template as a json template

    Parameters
    ----------
    dataset: pydicom.dataset.Dataset
        Input data. Usually read with pydicom.dcmread
    output_path: pathlike, optional
        Save json template to given file.
        Defaults to <default resource folder>/template_<hash>.json
    description: str, optional
        Save this description with the dataset. Default to None


    Returns
    -------
    str
        Json encoded representation of the metadata of this datatset. Includes
        private tags.

    """
    if not output_path:
        output_path = RESOURCE_PATH / f"tempate-{uuid.uuid4()}"

    # replace image data
    dataset = replace_pixel_data(dataset=dataset,
                                 image_path=RESOURCE_PATH / "skeleton_tiny.jpg")

    # Save dicom
    Template(template=dataset, description=description).save(output_path)


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
    pix = im.load()
    pixel_values = list(im.getdata())
    # convert image into numpy ndarray. use only R channel from RGB as this is
    # a greyscale image
    pix_np = np.array([x[0] for x in pixel_values])
    w, h = im.size  # Set dimensions
    pix_np.shape = (h, w)
    pix_np = rescale(pix_np, min=-2048, max=1000)  # make values a bit realistic for CT
    dataset.PixelData = pix_np.astype(np.int16).tostring()  # Not sure whether this can be other then int16,.
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
    range_offset = min - old_min

    ndarray = ndarray.astype(float)
    ndarray -= old_min  # translate to make based on 0
    ndarray *= range_scale  # scale to make range same size
    ndarray += min  # tranlate back to make old min fall on (new) min

    return ndarray.astype(old_dtype)


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
        return {"vr": input.VR, "InlineBinary": input.value.decode()}

    megabyte = 1024 * 1024
    return dataset.to_json(
        bulk_data_element_handler=just_decode_handler, bulk_data_threshold=megabyte * 3
    )
