from pathlib import Path
import pydicom
from dicomgenerator.reader import to_json
from dicomgenerator.resources import TEMPLATE_PATH

dcmfile = Path('/home/sjoerdk/code/python/packages/dicomgenerator/tests/resources/dcmfile1')
template_file = TEMPLATE_PATH / f"{dcmfile.name}.json"

# load dicom
ds = pydicom.dcmread(str(dcmfile))
output = to_json(ds)

with open(template_file, 'w') as f:
    f.write(output)

print(f"Wrote template to {template_file}")


