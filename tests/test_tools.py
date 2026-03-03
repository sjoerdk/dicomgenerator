import pytest

from dicomgenerator.generators import quick_dataset


def test_quick_dataset():
    ds = quick_dataset(PatientName="Jane", StudyDescription="Test")
    assert ds.PatientName == "Jane"
    assert ds.StudyDescription == "Test"
    with pytest.raises(ValueError):
        quick_dataset(unknown=1)
