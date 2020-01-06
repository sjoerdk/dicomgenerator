from pathlib import Path
import pydicom
from dicomgenerator.importer import to_json, Template, save_as_template
from dicomgenerator.resources import TEMPLATE_PATH
from tests import RESOURCE_PATH

"""Read in a dicom file, replace image data and save as a template in this libs
TEMPLATE_PATH dir.

TODO: Bit messy writing files directly into source. Future improvement should
be to manage template collection separately from this lib. 
"""

template_file = TEMPLATE_PATH / "test.json"

save_as_template(dataset=pydicom.dcmread(str(RESOURCE_PATH / 'dcmfile1')),
                 description='a test file template',
                 output_path=template_file)

print(f"Wrote template to {template_file}")
