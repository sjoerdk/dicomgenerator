import shutil

import pytest
import pydicom

from tests import RESOURCE_PATH


@pytest.fixture()
def a_dataset_path(tmp_path):
    """Path to a copy of a valid DICOM dataset"""
    a_dir = tmp_path / "datasets"
    a_dir.mkdir()
    dataset_path = a_dir / "dcmfile1"
    shutil.copy(str(RESOURCE_PATH / "dcmfile1"), str(dataset_path))
    return dataset_path


@pytest.fixture()
def a_dataset():
    """A DICOM dataset read from disk"""
    return pydicom.dcmread(RESOURCE_PATH / "dcmfile1")
