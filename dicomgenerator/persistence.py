"""Functions and classes for reading, writing and editing datasets"""
import json

from pydicom.dataset import Dataset


class JSONDataset:
    """A pydicom dataset that you can persist to disk in a human-readable way

    Facilitates dataset editing
    """

    def __init__(self, dataset):
        self.dataset = dataset

    @classmethod
    def load(cls, handle):
        """Load from json file"""
        return cls.from_dict(json.load(handle))

    def save(self, handle):
        """Save to file in json format"""
        handle.write(json.dumps(self.as_dict(), indent=4))

    @classmethod
    def from_dict(cls, dataset_dict):
        return cls(dataset=Dataset.from_json(dataset_dict))

    def as_dict(self):
        return self.dataset.to_json_dict()
