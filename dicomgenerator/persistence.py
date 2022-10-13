"""Functions and classes for reading, writing and editing datasets"""
import json

from pydicom.dataset import Dataset


class EditableDataset:
    """A pydicom dataset that you can persist to disk in a human-readable way

    Facilitates dataset editing. For example to create templates from actual data
    or examples to test deidentification
    """

    def __init__(self, dataset):
        self.dataset = dataset

    @classmethod
    def load(cls, handle):
        """Load from json file"""
        return Dataset.from_json(json.load(handle))

    def save(self, handle):
        """Save to file in json format"""

        def formatted_json(*args, **kwargs):
            kwargs.update({"indent": 4})
            return json.dumps(*args, **kwargs)

        handle.write(self.dataset.to_json(dump_handler=formatted_json))
