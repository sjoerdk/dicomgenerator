"""Functions and classes for reading, writing and editing datasets"""
import json

from pydicom.dataset import Dataset


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
