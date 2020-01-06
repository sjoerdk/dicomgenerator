import json
from copy import deepcopy
from pathlib import Path

import pydicom
import pytest
from pydicom.dataset import Dataset

from dicomgenerator.importer import to_json, save_as_template, Template
from tests import RESOURCE_PATH


@pytest.fixture()
def a_dataset():
    return pydicom.dcmread(str(RESOURCE_PATH / 'dcmfile1'))


def test_reader(a_dataset):
    """Simple load to from dicom json"""
    output = to_json(a_dataset)
    loaded = Dataset.from_json(json.loads(output))
    assert len(loaded) == 106


def test_reader_pixeldata(a_dataset):
    """Check json serialization of pixeldata"""
    only_pixeldata = Dataset()
    only_pixeldata.PixelData = a_dataset.PixelData
    only_pixeldata.SpecificCharacterSet = a_dataset.SpecificCharacterSet
    output = to_json(only_pixeldata)
    loaded = Dataset.from_json(json.loads(output))
    assert loaded.PixelData == a_dataset.PixelData


def test_reconstruct(a_dataset):
    """Read dataset, serialise, then deserialise"""
    original = list(deepcopy(a_dataset))
    reloaded = Dataset.from_json(to_json(a_dataset))

    # make sure all elements that were included are the same as original
    for data_element in reloaded:
        assert data_element in original


def test_template_load_save(a_dataset, tmpdir):
    output_path = Path(tmpdir) / 'test.json'

    description = 'test_description'
    save_as_template(dataset=a_dataset, description=description,
                     output_path=output_path)

    loaded = Template.load(output_path)
    assert loaded.template == a_dataset
    assert description == description


