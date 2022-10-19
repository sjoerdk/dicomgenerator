from click.testing import CliRunner
import dicomgenerator.cli as cli
from dicomgenerator.annotation import AnnotatedDataset, FileAnnotatedDataset


def test_cli_to_json(a_dataset_path):
    runner = CliRunner()
    assert len(list(a_dataset_path.parent.glob("*"))) == 1  # one file in dir

    result = runner.invoke(cli.to_json, [str(a_dataset_path)], catch_exceptions=False)
    assert result.exit_code == 0  # call should succeed
    with open(str(a_dataset_path) + "_template.json") as f:
        annotated = AnnotatedDataset.load(f)  # json dataset should be written
    assert annotated.description == "Converted"


def test_cli_to_dataset(tmp_path, a_dataset_path):
    """Test loading from dicom and saving as json"""
    fad = FileAnnotatedDataset.from_dicom_path(a_dataset_path)

    # by default this
    saved_path = fad.save_to_path()
    with open(saved_path) as f:
        loaded = AnnotatedDataset.load(f)
    for element in fad.dataset:
        assert element == loaded.dataset[element.tag]
