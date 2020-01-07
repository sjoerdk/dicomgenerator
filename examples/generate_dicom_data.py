from pathlib import Path

import pydicom

from dicomgenerator.exporter import export
from dicomgenerator.factory import CTDatasetFactory


"""Generate some CT-like DICOM files """

output_dir = Path('/tmp/dummy_dicom')


def generate_some_dicom_files(output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    filenames = [f"dcmfile{x}" for x in range(5)]
    for filename in filenames:
        export(dataset=CTDatasetFactory(), path=output_dir / filename)

    print(f"Wrote {len(filenames)} files to {output_dir}")


def generate_file_with_specifics(output_path):
    """Generate a dicom file, set specific tags. All tags supported by pydicom
    can be set here"""
    export(dataset=CTDatasetFactory(PatientSex='M',
                                    PatientName='Smith^Harry',
                                    PatientIdentityRemoved='NO'),
           path=output_path)

    print(f"Wrote file to {output_path}")


# generate_file_with_specifics(output_path=output_dir / 'dicomfile_m')
generate_some_dicom_files(output_dir)
