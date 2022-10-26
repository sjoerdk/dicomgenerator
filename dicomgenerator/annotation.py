"""Code for adding annotations to datasets"""
from typing import Any, Union

from pydicom.datadict import dictionary_keyword
from pydicom.dataset import Dataset
from pydicom.tag import Tag

from dicomgenerator.persistence import FileJSONDataset, JSONDataset


class AnnotatedDataset(JSONDataset):

    json_keyword = "annotation"  # serialize annotations under this key
    json_tag_name_keyword = "tag_name"  # put dicom tag name under this key

    def __init__(self, dataset, description="No description", annotations=None):
        """A dataset with a description and annotations associated with each tag

        Can be persisted to disk in a human-readable and editable way. Leverages
        pydicom's Dataset.to_json() method, but adds annotation field
        and tag name field for easier reading of the tag (pydicom only persists
        tag values like '00100010').

        Parameters
        ----------
        dataset: Dataset
            The pydicom dataset
        description: str
            Description of this dataset
        annotations: Dict[TagLike, Union[JSONSerializable, str, int, Dict]]
            Annotations per tag. TagLike can be DICOM tag name such as 'PatientID'
            ,hex such as '0x0010,0x0012' or a Tag object. Value is JSONSerializable
            or anything that you can put in json.dumps()
        """

        super().__init__(dataset)
        self.description = description
        if not annotations:
            self.annotations = {}
        else:
            self.annotations = {Tag(x): y for x, y in annotations.items()}

    def all_tags(self):
        """Returns tuples (DicomElement, Annotation) for all tags"""
        yield from ((x, self.annotations.get(x.tag)) for x in self.dataset)

    def get_annotation(self, key: Union[str, int]) -> Any:
        return self.annotations.get(Tag(key))

    @staticmethod
    def annotation_to_json_obj(annotation):
        """Make sure annotation can be put in json.dumps()"""
        if hasattr(annotation, "to_json_dict"):
            return annotation.to_json_dict()
        else:
            return annotation

    def to_json_dict(self):
        dataset = self.dataset.to_json_dict()
        for tag, element_dict in dataset.items():
            element_dict[self.json_keyword] = self.annotation_to_json_obj(
                self.get_annotation(tag)
            )
            try:
                element_dict[self.json_tag_name_keyword] = dictionary_keyword(tag)
            except KeyError:
                element_dict[self.json_tag_name_keyword] = "Unknown"

        return {"description": self.description, "dataset": dataset}

    @classmethod
    def parse_annotation(cls, annotation_json_obj):
        """Process raw annotation object. For overwriting in child classes"""
        return annotation_json_obj

    @classmethod
    def from_json_dict(cls, dict_in):
        dataset_dict = dict_in["dataset"]
        annotations = {}
        for tag, element_dict in dataset_dict.items():
            if element_dict.get(cls.json_keyword):
                annotations[Tag(tag)] = cls.parse_annotation(
                    element_dict.get(cls.json_keyword)
                )
            del element_dict[cls.json_keyword]
            del element_dict[cls.json_tag_name_keyword]

        return cls(
            dataset=Dataset.from_json(dataset_dict),
            annotations=annotations,
            description=dict_in["description"],
        )


class FileAnnotatedDataset(FileJSONDataset):
    """AnnotatedDataset read from DICOM file on disk

    Makes conversion (DICOM -> Example DICOM) cleaner
    """

    json_dataset_class = AnnotatedDataset
