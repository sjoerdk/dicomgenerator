from dicomgenerator.dicom import VRs


def test_vrs():

    assert VRs.is_date_like("DT")
    assert not VRs.is_numeric("DT")

    assert VRs.is_numeric("DS")
    assert not VRs.is_date_like("DS")
