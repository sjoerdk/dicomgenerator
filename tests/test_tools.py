import pytest
from dicomgenerator.annotation import AnnotatedDataset
from dicomgenerator.generators import quick_dataset
from dicomgenerator.tools import to_annotated_dataset


def test_convert_dataset(a_dataset, tmpdir):
    folder = tmpdir.mkdir("templates_test")
    input_path = folder / "input.dcm"
    a_dataset.save_as(input_path)

    template_path = to_annotated_dataset(
        input_path=input_path, description="test convert"
    )

    # now check what has been written
    with open(template_path) as f:
        loaded = AnnotatedDataset.load(f)

    assert loaded.description == "test convert"
    for element in loaded.dataset:
        assert a_dataset[element.tag] == element


def test_quick_dataset():
    ds = quick_dataset(PatientName="Jane", StudyDescription="Test")
    assert ds.PatientName == "Jane"
    assert ds.StudyDescription == "Test"
    with pytest.raises(ValueError):
        quick_dataset(unknown=1)
