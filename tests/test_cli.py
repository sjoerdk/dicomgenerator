from click.testing import CliRunner
import dicomgenerator.cli as cli
from dicomgenerator.annotation import AnnotatedDataset


def test_cli_to_json(a_dataset_path):
    runner = CliRunner()
    assert len(list(a_dataset_path.parent.glob("*"))) == 1  # one file in dir

    result = runner.invoke(cli.to_json, [str(a_dataset_path)], catch_exceptions=False)
    assert result.exit_code == 0  # call should succeed
    with open(str(a_dataset_path) + "_template.json") as f:
        annotated = AnnotatedDataset.load(f)  # json dataset should be written
    assert annotated.description == "Converted"
