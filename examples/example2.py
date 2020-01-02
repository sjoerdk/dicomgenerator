import json
import pydicom

from dicomgenerator.reader import to_json
from pathlib import Path
from pydicom.dataset import Dataset
from tests import RESOURCE_PATH

"""
Read a dicom file, convert to json, convert back to dataset and then save.
Should still be a valid dicom file
"""

dcmfile = pydicom.dcmread(str(RESOURCE_PATH / 'dcmfile1'))
dcmfile_out = Path('/tmp/dcmfile1_mod')


output = to_json(dcmfile)
ds = Dataset.from_json(json.loads(output))

ds.is_implicit_VR = False
ds.is_little_endian = True

ds.save_as(str(dcmfile_out))
print(f'Wrote to {dcmfile_out}')
