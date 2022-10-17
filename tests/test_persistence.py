from io import StringIO

from dicomgenerator.persistence import JSONDataset
from dicomgenerator.annotation import AnnotatedDataset


def test_editable_dataset_save_load(a_dataset):
    """Save and then load again"""
    file = StringIO()
    ds = JSONDataset(dataset=a_dataset)
    ds.save(file)
    file.seek(0)

    for loaded_tag in JSONDataset.load(file).dataset:
        assert ds.dataset[loaded_tag.tag] == loaded_tag


def test_annotated_dataset(a_dataset):
    """Make annotated dataset go through basic functions"""
    an_annotation = "a patient annotation"
    ad = AnnotatedDataset(
        a_dataset,
        description="test description",
        annotations={"PatientID": an_annotation},
    )

    # check getting annotations
    annotations = [x for x in ad.all_tags()]
    _, annotation = annotations[23]
    assert annotation == an_annotation
    assert ad.get_annotation("PatientID") == an_annotation

    # check writing to file
    file = StringIO()
    ad.save(file)
    file.seek(0)
    content = file.read()
    assert an_annotation in content
    file.seek(0)

    # save and load should not have changed content
    loaded = AnnotatedDataset.load(file)
    assert loaded.get_annotation("PatientID") == an_annotation
    assert loaded.description == "test description"
    for element in ad.dataset:
        assert element == loaded.dataset[element.tag]
