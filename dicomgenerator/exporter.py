from pathlib import Path

from pydicom.dataset import Dataset


def export(dataset: Dataset, path: Path):
    """Save dataset to path in most common encoding """
    # set most common options
    dataset.is_little_endian = True
    dataset.is_implicit_VR = False

    dataset.save_as(str(path))
