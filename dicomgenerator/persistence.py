"""Functions and classes for reading, writing and editing datasets"""
import json
from pathlib import Path

import pydicom
from pydicom.dataset import Dataset

from dicomgenerator import logging

logger = logging.get_module_logger("annotation")


class JSONSerializable:
    """Something that you can persist to and from JSON"""

    def to_json_dict(self):
        """Object as a json-serializable dict"""
        raise NotImplementedError()

    @classmethod
    def from_json_dict(cls, json_dict):
        """Create instance of this object from json-serializable dict"""
        raise NotImplementedError()


class JSONDataset(JSONSerializable):
    """A pydicom dataset that you can persist to disk in a human-readable way

    Facilitates dataset editing
    """

    def __init__(self, dataset):
        self.dataset = dataset

    @classmethod
    def load(cls, handle):
        """Load from json file"""
        return cls.from_json_dict(json.load(handle))

    def save(self, handle):
        """Save to file in json format"""
        handle.write(json.dumps(self.to_json_dict(), indent=4))

    @classmethod
    def from_json_dict(cls, dataset_dict):
        return cls(dataset=Dataset.from_json(dataset_dict))

    def to_json_dict(self):
        return self.dataset.to_json_dict()


class FromDicomFileMixin(JSONDataset):
    """Links JSONSerializable to file on disk

    Makes conversion (DICOM -> JSON) cleaner:
    * read/parse from dicom file on disk
    * save to json file next to input file by default

    Keeping these separate to add to child classes if needed but
    not clutter the main class with often-unneeded IO stuff
    """

    source_file_path: Path

    @classmethod
    def from_dicom_path(cls, source_file_path: Path):
        """Init from DICOM file on disk"""

        logger.info(f"Reading DICOM dataset from '{source_file_path}'")
        klass = cls(dataset=pydicom.dcmread(source_file_path))
        klass.source_file_path = source_file_path
        return klass

    def save_to_path(self, save_path=None):
        """Save to disk. Next to input file by default"""
        if save_path:
            save_path = Path(save_path)
        else:
            source = Path(self.source_file_path)
            save_path = source.parent / (source.stem + "_template.json")
        with open(save_path, "w") as f:
            self.save(f)
        logger.info(f"Wrote {self} to '{save_path}'")
        return save_path
