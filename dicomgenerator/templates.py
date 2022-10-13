"""Templates for generating specific types of DICOM"""
import factory

from dicomgenerator.generators import DatasetFactory
from dicomgenerator.resources import TEMPLATE_PATH


class CTDatasetFactory(DatasetFactory):
    """A dataset based on a TOSHIBA AQUILIONXL dicom image

    generates random values for dates and times, patient name and several UIDs
    Image data is fake
    """

    class Meta:
        exclude = ("base_study_date", "base_study_time")

    template_path = str(TEMPLATE_PATH / "ct_toshiba_aquilion.json")
    AccessionNumber = "1234"

    base_study_date = factory.Faker("dicom_date")

    StudyDate = factory.LazyAttribute(lambda x: x.base_study_date)
    SeriesDate = factory.LazyAttribute(lambda x: x.base_study_date)
    AcquisitionDate = factory.LazyAttribute(lambda x: x.base_study_date)
    ContentDate = factory.LazyAttribute(lambda x: x.base_study_date)
    ScheduledProcedureStepStartDate = factory.LazyAttribute(lambda x: x.base_study_date)
    ScheduledProcedureStepEndDate = factory.LazyAttribute(lambda x: x.base_study_date)
    PerformedProcedureStepEndDate = factory.LazyAttribute(lambda x: x.base_study_date)

    base_study_time = factory.Faker("dicom_time")

    StudyTime = factory.LazyAttribute(lambda x: x.base_study_time)
    SeriesTime = factory.LazyAttribute(lambda x: x.base_study_time)
    AcquisitionTime = factory.LazyAttribute(lambda x: x.base_study_time)
    ContentTime = factory.LazyAttribute(lambda x: x.base_study_time)
    ScheduledProcedureStepStartTime = factory.Faker("dicom_time")
    ScheduledProcedureStepEndTime = factory.Faker("dicom_time")
    PerformedProcedureStepEndTime = factory.LazyAttribute(lambda x: x.base_study_time)

    PatientName = factory.Faker("dicom_person_name")

    SOPInstanceUID = factory.Faker("dicom_ui")
    StudyInstanceUID = factory.Faker("dicom_ui")
    SeriesInstanceUID = factory.Faker("dicom_ui")
    FrameOfReferenceUID = factory.Faker("dicom_ui")

    PatientIdentityRemoved = "NO"
