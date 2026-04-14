"""Classes and functions for working with Dataset pixeldata"""
import hashlib
from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Optional, Tuple

import numpy as np
from PIL import Image
from numpy.random import random
from pydicom import Dataset, FileMetaDataset
from pydicom.uid import ExplicitVRLittleEndian

from dicomgenerator.logging import get_module_logger
from dicomgenerator.resources import RESOURCE_PATH

logger = get_module_logger("pixeldata")


class PhotoMetricInterpretation(Enum):
    """Valid values for (0028,0004) Photometric Interpretation

    Needed for https://pydicom.github.io/pydicom/stable/reference/
    generated/pydicom.pixels.set_pixel_data.html
    Apparently pydicom does not encode this? Encoding here for now then.
    """

    MONOCHROME1 = "MONOCHROME1"
    MONOCHROME2 = "MONOCHROME2"
    PALETTE_COLOR = "PALETTE COLOR"
    RGB = "RGB"
    YBR_FULL = "YBR_FULL"
    YBR_FULL_422 = "YBR_FULL_422"


def replace_pixel_data(dataset, image_path=None):
    """Replace the DICOM PixelData tag with the data from image_path

    Parameters
    ----------
    dataset: pydicom.dataset.Dataset
        Replace pixel data in this dataset, if pixeldata exists
    image_path:
        pathlike to rgb image readable with pillow, optional

    Returns
    -------
    pydicom.dataset.Dataset
        With replaced PixelData and Columns and Rows changed to match
    """
    if "PixelData" not in dataset:
        return dataset  # No pixeldata, nothing needs to be done

    if not image_path:
        image_path = RESOURCE_PATH / "skeleton_tiny.jpg"

    logger.info(f'Replacing image data with image at "{image_path}"')

    im = Image.open(image_path)
    pixel_values = list(im.getdata())
    # convert image into numpy ndarray. use only R channel from RGB as this is
    # a greyscale image
    pix_np = np.array([x[0] for x in pixel_values])
    w, h = im.size  # Set dimensions
    pix_np.shape = (h, w)
    pix_np = rescale(pix_np, min_val=-2048, max_val=1000)  # make pixel_array CT-like
    dataset.PixelData = pix_np.astype(
        np.int16
    ).tobytes()  # Not sure whether this can be other than int16.
    dataset.Rows, dataset.Columns = pix_np.shape
    return dataset


def rescale(ndarray, min_val, max_val):
    """Rescale pixel_array of ndarray linearly so min of ndarray is min, max is max

    Parameters
    ----------
    ndarray: numpy nd array
    min_val: int
    max_val: int

    Returns
    -------
    numpy ndarray

    """

    old_max = ndarray.max()
    old_min = ndarray.min()
    old_range = old_max - old_min
    old_dtype = ndarray.dtype
    new_range = max_val - min_val
    range_scale = new_range / old_range

    ndarray = ndarray.astype(float)
    ndarray -= old_min  # translate to make based on 0
    ndarray *= range_scale  # scale to make range same size
    ndarray += min_val  # translate back to make old min fall on (new) min

    return ndarray.astype(old_dtype)


def generate_image(width=128, height=128):
    """Create an image that can be written to pixeldata"""
    image = Image.effect_noise((width, height), 50)
    return image


def effect_noise_seeded(width, height, sigma, seed=None):
    rng = np.random.default_rng(seed)
    noise = rng.normal(loc=128, scale=sigma, size=(height, width))
    noise = np.clip(noise, 0, 255).astype(np.uint8)
    return Image.fromarray(noise, mode="L")


def add_pixel_data_2d(dataset: Dataset, pixel_array: np.ndarray, dtype: str):
    """Write image into pixel data. Set rows and columns

    Warning
    -------
    Modifies dataset.file_meta and sets TransferSyntaxUID. Is not completely respectful
    of DICOM conformity. Meant for testing and debugging pixel processors.
    """
    ds = dataset
    ds.file_meta = FileMetaDataset()
    ds.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

    num_bits = np.iinfo(dtype).bits

    ds.BitsAllocated = num_bits
    ds.BitsStored = num_bits
    ds.HighBit = ds.BitsStored - 1
    ds.PixelRepresentation = 0

    ds.SamplesPerPixel = 1
    ds.PhotometricInterpretation = PhotoMetricInterpretation.MONOCHROME2.value

    ds.PixelData = pixel_array.tobytes()
    ds["PixelData"].VR = "OB"
    ds.Rows = pixel_array.shape[0]  # 320 pixels
    ds.Columns = pixel_array.shape[1]  # 480 pixels

    # add padding for DICOM conformance
    if pixel_array.size % 2 == 1:
        # Trailing padding required to make the length an even number of bytes
        ds.PixelData = b"".join((pixel_array.tobytes(), b"\x00"))

    return ds


def md5_int(string_in):
    """Consistent int for any string"""
    return int(hashlib.md5(string_in.encode()).hexdigest(), 16)


def draw_noise(
    height: int, width: int, dtype: str, seed: Optional[str] = None
) -> np.ndarray:
    """Return an array containing random values between 0 and maximum for the given
    datatype.

    Parameters
    ----------
    height
    width
    dtype
    seed:
        Optional random seed to use for generation. Two calls to draw_noise with seed
        and other parameters unchanged should result in identical ndarrays.
        Defaults to empty string, in which case no seed is set and the resulting noise
        is random

    Returns
    -------
    numpy ndarray
        a 2-d array

    """
    max_value = np.iinfo(dtype).max
    if seed:
        rng = np.random.default_rng(md5_int(seed))
        arr = rng.random((height, width))
    else:
        arr = random((height, width))

    # Convert to the required `dtype` and set the maximum `value`
    arr = arr * max_value
    return arr.astype(dtype)


@dataclass
class Extent:
    """A region in 2D space"""

    start_x: int
    end_x: int
    start_y: int
    end_y: int


@dataclass
class Block:
    """A region in 2D space"""

    origin_x: int
    origin_y: int
    height: int
    width: int

    def as_extent(self) -> Extent:
        """Recode here so I never have to repeat this"""
        return Extent(
            start_x=self.origin_x,
            end_x=self.origin_x + self.height,
            start_y=self.origin_y,
            end_y=self.origin_y + self.width,
        )

    def as_2d_slice(self) -> Tuple[slice, slice]:
        """To be used in numpy 2d arrays directly"""
        return (
            slice(self.origin_x, self.origin_x + self.height),
            slice(self.origin_y, self.origin_y + self.width),
        )


def add_blocks(dataset: Dataset, blocks: Iterable[Block], value=0) -> Dataset:
    """Fill dataset PixelData area within blocks with value

    Returns
    -------
    Dataset:
        Where pixeldata has been modified to have value at all places indicated by
        blocks

    Raises
    ------
    OverflowError:
        If value does not fit inside the bit depth of the dataset's pixel data
    """
    pixel_array = dataset.pixel_array
    for block in blocks:
        check_bounds(block, pixel_array)
        pixel_array[
            block.origin_y : block.origin_y + block.height,
            block.origin_x : block.origin_x + block.width,
        ] = value
    dataset.PixelData = pixel_array.tobytes()

    return dataset


def check_bounds(block: Block, pixel_array: np.ndarray):
    """Raise exception if block is no fully within the bounds of pixel array

    In the case of dicom 2d pixeldata regions, a block that is out of bounds is always
    a user error and should not be allowed

    Raises
    ------
    ValueError
        If block is not within pixel array dimensions
    """
    extent = block.as_extent()
    (imsize_x, imsize_y) = pixel_array.shape

    if extent.start_x < 0:
        raise ValueError(
            f"Block start {extent.start_x} is below 0. This does not make "
            f"sense for 2d image data"
        )
    if extent.start_y < 0:
        raise ValueError(
            f"Block start {extent.start_y} is below 0. This does not make "
            f"sense for 2d image data"
        )
    if extent.end_x > imsize_x or extent.end_y > imsize_y:
        raise ValueError(
            f"Block {block} extends beyond image size {imsize_x, imsize_y}"
            f"This does not make sense"
        )
