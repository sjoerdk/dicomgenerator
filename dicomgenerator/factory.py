"""Functions to create pydicom datasets to look like different types of DICOM
"""

import json
import datetime
import factory
import pydicom
from pydicom.dataset import Dataset

from dicomgenerator.resources import TEMPLATE_PATH
from dicomgenerator.settings import DICOM_GENERATOR_ROOT_UID
from factory.fuzzy import FuzzyDate
from faker.providers import BaseProvider
from faker import Faker
from pydicom.uid import generate_uid
from random import randint


class FuzzyDICOMDateString(FuzzyDate):
    """A valid DICOM value for a DA (Date) type value

    see
    http://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.2.html
    """

    def fuzz(self):
        date = super(FuzzyDICOMDateString, self).fuzz()
        return date.strftime("%Y%m%d")


class DatasetFactory(factory.Factory):
    """Generates a pydicom dataset based on a json-dicom template

    """
    # This bytes preamble is actually required. DICOM is strange. See.
    # http://dicom.nema.org/dicom/2013/output/chtml/part10/chapter_7.html
    preamble = b"\0" * 128

    class Meta:
        model = pydicom.dataset.Dataset

    class Params:
        base_study_date = FuzzyDICOMDateString(
            start_date=datetime.date(2008, 1, 1), end_date=datetime.date(2013, 4, 16)
        )

    @classmethod
    def _create(cls, model_class, *args, template_path, **kwargs):
        """Instead of creating a clean instance, will load pydicom Dataset
        instance from template, then overwrite loaded values with any kwargs

        """
        obj = model_class.from_json(
            *args, json_dataset=json.load(open(template_path, "r")),
        )
        for key, value in kwargs.items():  # overwrite loaded args with kwargs
            setattr(obj, key, value)
        return obj

    template_path = ""


class DICOMVRProvider(BaseProvider):
    """Generates valid values for several DICOM Value representations (VR)

    see
    http://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.2.html

    """

    locale = "nl_NL"

    def dicom_person_name(self):
        """Something like 'Doe^Jane' or 'Vries^Sep de' (VR = PN)

        Returns
        -------
        str
        """
        faker = Faker(locale=self.locale)
        return f"{faker.last_name()}^{faker.first_name()}"

    def dicom_time(self):
        """Dicom time string. Like 14350204.123 (VR = TM)

        Returns
        -------
        str
        """
        return (
            datetime.time(
                hour=randint(0, 23),
                minute=randint(0, 59),
                second=randint(0, 59),  # DICOM spec says 0-60. serious?
            ).strftime("%H%M%S")
            + "."
            + str(randint(100, 999))
        )

    def dicom_date(self):
        """Dicom date string. Like 20120425 (VR = DA)

        Returns
        -------
        str
        """
        date = FuzzyDate(
            start_date=datetime.date(2008, 1, 1), end_date=datetime.date(2013, 4, 16)
        ).fuzz()
        return date.strftime("%Y%m%d")

    def dicom_ui(self):
        """Valid DICOM UID (VR = UI)

        Returns
        -------
        str
        """

        return str(generate_uid(prefix=DICOM_GENERATOR_ROOT_UID))


factory.Faker.add_provider(DICOMVRProvider)


class CTDatasetFactory(DatasetFactory):
    """A dataset based on a TOSHIBA AQUILIONXL dicom image

    generates random values for dates and times, patient name and several UIDs
    Image data is fake
    """

    class Meta:
        exclude = ("base_study_date", "base_study_time")

    template_path = TEMPLATE_PATH / "ct_toshiba_aquilion.json"
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
