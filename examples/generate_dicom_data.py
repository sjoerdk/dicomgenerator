import uuid
from pathlib import Path

from dicomgenerator.export import export
from dicomgenerator.templates import CTDatasetFactory

"""Generate some CT-like DICOM files """

output_dir = Path("/tmp/dummy_dicom")


def generate_some_dicom_files(output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    filenames = [f"dcmfile{x}" for x in range(5, 10)]
    for filename in filenames:
        export(
            dataset=CTDatasetFactory(PatientID="patient2"), path=output_dir / filename
        )

    print(f"Wrote {len(filenames)} files to {output_dir}")


def generate_file_with_specifics(output_path):
    """Generate a dicom file, set specific tags. All tags supported by pydicom
    can be set here
    """
    export(
        dataset=CTDatasetFactory(
            PatientSex="M", PatientName="Smith^Harry", PatientIdentityRemoved="NO"
        ),
        path=output_path,
    )

    print(f"Wrote file to {output_path}")


def generate_dicom_structure(structure, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for patient, studies in structure.items():
        for study, seriess in studies.items():
            for series in seriess:
                for _ in range(2):
                    count = count + 1
                    export(
                        dataset=CTDatasetFactory(
                            PatientID=patient,
                            StudyInstanceUID=study,
                            SeriesInstanceUID=series,
                        ),
                        path=output_dir / str(uuid.uuid4()),
                    )

    print(f"Wrote {count} files to {output_dir}")


structure = {
    "patient1": {"11111.1": ["2222.1", "2222.2"], "11111.2": ["2222.1"]},
    "patient2": {"11111.1": ["2222.1"], "11111.2": ["2222.1", "2222.2", "2222.3"]},
}
