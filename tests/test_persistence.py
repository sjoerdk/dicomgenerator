from io import StringIO

from dicomgenerator.persistence import EditableDataset


def test_editable_dataset_save_load(a_dataset):
    """Save and then load again"""
    file = StringIO()
    ds = EditableDataset(dataset=a_dataset)
    ds.save(file)
    file.seek(0)

    for loaded_tag in EditableDataset.load(file):
        assert ds.dataset[loaded_tag.tag] == loaded_tag
