import pytest
import pydicom

from tests import RESOURCE_PATH


@pytest.fixture()
def a_dataset():
    """A DICOM dataset read from disk"""
    return pydicom.dcmread(str(RESOURCE_PATH / "dcmfile1"))
