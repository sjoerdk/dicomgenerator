"""Functions and classes for reading, writing and editing datasets"""
import json
from typing import Any, Union

from pydicom.dataset import Dataset
from pydicom.tag import Tag


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

    def to_dict(self):
        return


class AnnotatedDataset(EditableDataset):
    """A dataset with a description and annotations associated with each tag"""

    json_keyword = "annotation"  # serialize annotations under this key

    def __init__(self, dataset, description="No description", annotations=None):
        """

        Parameters
        ----------
        dataset: Dataset
            The pydicom dataset
        description: str
            Description of this dataset
        annotations: Dict[TagLike, JsonSerializable]
            Annotations per tag. TagLike can be DICOM tag name such as 'PatientID'
            ,hex such as '0x0010,0x0012' or a Tag object. JsonSerializable is
            anything that you can put in json.dumps()
        """

        super().__init__(dataset)
        self.description = description
        if not annotations:
            self.annotations = {}
        else:
            self.annotations = {Tag(x): y for x, y in annotations.items()}

    def __iter__(self):
        """Returns tuples (DicomElement, Annotation)"""
        yield from ((x, self.annotations.get(x.tag)) for x in self.dataset)

    def get_annotation(self, key: Union[str, int]) -> Any:
        return self.annotations.get(Tag(key))

    def save(self, handle):
        """Save to file in json format"""

        def annotation_dump_handler(*args, **kwargs):
            """Dumps to human-readable json. Adds annotations to each element"""
            tags_dict = args[0]
            for tag, element_dict in tags_dict.items():
                element_dict[self.json_keyword] = self.get_annotation(tag)
            kwargs.update({"indent": 4})
            return json.dumps(*args, **kwargs)

        handle.write(json.dumps(self.as_dict(), indent=4))

    def as_dict(self):
        dataset = self.dataset.to_json_dict()
        for tag, element_dict in dataset.items():
            element_dict[self.json_keyword] = self.get_annotation(tag)
        return {"description": self.description, "dataset": dataset}

    @classmethod
    def from_dict(cls, dict_in):
        dataset_dict = dict_in["dataset"]
        annotations = {}
        for tag, element_dict in dataset_dict.items():
            if element_dict.get(cls.json_keyword):
                annotations[Tag(tag)] = element_dict.get(cls.json_keyword)
            del element_dict[cls.json_keyword]

        return cls(
            dataset=Dataset.from_json(dataset_dict),
            annotations=annotations,
            description=dict_in["description"],
        )

    @classmethod
    def load(cls, handle):
        """Load from json file"""
        return cls.from_dict(json.load(handle))
