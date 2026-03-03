"""Functions and classes for turning existing DICOM files into editable datasets
and templates
"""


def dataset_to_json(dataset, replace_image_data=True, description="Converted"):
    """Turn dataset into a template. Replaces image data with tiny dummy image
    by default
    """
    raise NotImplementedError(
        "Removed after v0.9. Use pydicom 3 functions: "
        "https://pydicom.github.io/pydicom/stable/tutorials/dicom_json.html"
    )


def to_annotated_dataset(
    input_path, output_path=None, description="Converted", replace_pixel_data=False
):
    raise NotImplementedError(
        "Removed after v0.9. Use pydicom 3 functions: "
        "https://pydicom.github.io/pydicom/stable/tutorials/dicom_json.html"
    )
