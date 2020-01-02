"""
For switching actual image data with dummy image, for use as test data in public
repo
See https://repos.diagnijmegen.nl/trac/ticket/8992

"""
import matplotlib.pyplot as plt
import numpy as np
import pydicom

from dicomgenerator.resources import RESOURCE_PATH
from PIL import Image
from pathlib import Path


def rescale(ndarray, min, max):
    """Rescale values of ndarray so min of ndarray is min, max is max"""

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


dcmfile = Path('/home/sjoerdk/code/python/packages/anonqa/tests/resources/dcmfile1')
dcmfile_out = Path('/home/sjoerdk/code/python/packages/anonqa/tests/resources/dcmfile1_mod')
imagefile = RESOURCE_PATH / 'skeleton.jpg'

# load image
im = Image.open(imagefile)
pix = im.load()
pixel_values = list(im.getdata())

# load dicom
ds = pydicom.dcmread(str(dcmfile))
data = ds.pixel_array

del ds.PixelData
test = ds.to_json()

# convert image into numpy ndarray. use only R channel from RGB as this is
# a greyscale image
pix_np = np.array([x[0] for x in pixel_values])
w, h = im.size   # Set dimensions
pix_np.shape = (h, w)


pix_np = rescale(pix_np, min=-2048, max=1000)  # make values a bit realistic for CT

ds.PixelData = pix_np.astype(np.int16).tostring()  # Not sure whether this can be other then int16,.
ds.Rows, ds.Columns = pix_np.shape

plt.imshow(ds.pixel_array, cmap=plt.cm.bone)
plt.show()
#ds.save_as(str(dcmfile_out))
#print(f'Wrote to {dcmfile_out}')