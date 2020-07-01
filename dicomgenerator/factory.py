"""Functions to create pydicom datasets to look like different types of DICOM
"""

import json
import datetime
import factory
import pydicom
import random

from factory.random import get_random_state
from pydicom.datadict import dictionary_VR
from pydicom.tag import Tag

from dicomgenerator.dicom import VR, VRs
from dicomgenerator.exceptions import DICOMGeneratorException
from dicomgenerator.resources import TEMPLATE_PATH
from dicomgenerator.settings import DICOM_GENERATOR_ROOT_UID
from factory.fuzzy import FuzzyDate
from faker.providers import BaseProvider
from faker import Faker
from pydicom.uid import generate_uid


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
                hour=factory.random.randgen.randint(0, 23),
                minute=factory.random.randgen.randint(0, 59),
                second=factory.random.randgen.randint(0, 59),  # DICOM spec says 0-60?
            ).strftime("%H%M%S")
            + "."
            + str(factory.random.randgen.randint(100, 999))
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
        """generate Valid DICOM UID (VR = UI)

        Uses factory boy random seed, so setting seed in test yields the same
        UID value each time

        Returns
        -------
        str
        """
        return str(generate_uid(
            prefix=DICOM_GENERATOR_ROOT_UID,
            entropy_srcs=[str(factory.random.randgen.getrandbits(100))]),
                   )


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


class DataElementFactory(factory.Factory):
    """Generates pydicom DataElements.

    Will always match VR and random value to given values

    >>> DataElementFactory(tag='PatientName').vr = 'PN'
    >>> DataElementFactory(tag='PatientName').value = 'JONES^Sarah'

    You can still set custom values as well:
    >>> DataElementFactory(tag='PatientName', value='123').value = '123'

    Notes
    -----
    For an unknown tag without an explicit VR, this factory will assign a
    LongString (LO) VR:
    >>> DataElementFactory(tag=('ee011020')).VR = 'LO'

    If this is not what you want, pass an explicit VR:
    >>> DataElementFactory(tag=('ee011020'), VR='SL', value=-10.2)
    """

    class Meta:
        model = pydicom.dataelem.DataElement

    tag = Tag('PatientID')

    @factory.lazy_attribute
    def VR(self):
        """Find the correct Value Representation for this tag from pydicom"""
        try:
            return dictionary_VR(Tag(self.tag))
        except KeyError as e:
            # unknown tag. Just return set value, assuming user want to just
            # get on with it
            return VRs.LongString.short_name

    @factory.lazy_attribute
    def value(self):
        """Generate a valid mock value for this type of VR

        Raises
        ------
        DataElementFactoryException
            If a value cannot be generated
        """

        vr = VRs.short_name_to_vr(self.VR)
        if vr == VRs.ApplicationEntity:
            return "MockEntity"
        elif vr == VRs.AgeString:
            return f"{factory.random.randgen.randint(0,120):03d}Y"
        elif vr == VRs.AttributeTag:
            return 0x0010, 0x0010
        elif vr == VRs.CodeString:
            return "MockCodeString"
        elif vr == VRs.Date:
            return factory.Faker("dicom_date").generate({})
        elif vr == VRs.DecimalString:
            return "+10.4"
        elif vr == VRs.DateTime:
            return factory.Faker("dicom_date").generate({}) +\
                   factory.Faker("dicom_time").generate({})
        elif vr == VRs.FloatingPointSingle:
            return 1.1
        elif vr == VRs.FloatingPointDouble:
            return 1.123
        elif vr == VRs.IntegerString:
            return f"{factory.random.randgen.randint(-2**31,2**31)}"
        elif vr == VRs.LongString:
            return factory.Faker('sentence').generate()[:64]
        elif vr == VRs.LongText:
            return factory.Faker('text').generate()[:10240]
        elif vr == VRs.OtherByteString:
            return b'\x13\00'
        elif vr == VRs.OtherDoubleString:
            return "MockDoubleString"
        elif vr == VRs.OtherFloatString:
            return "MockFloatString"
        elif vr == VRs.OtherWordString:
            return "MockOtherWordString"
        elif vr == VRs.PersonName:
            return factory.Faker("dicom_person_name").generate({})
        elif vr == VRs.ShortString:
            return "MockShortString"
        elif vr == VRs.SignedLong:
            return factory.random.randgen.randint(-2**32, 2**32)
        elif vr == VRs.Sequence:
            return []
        elif vr == VRs.SignedShort:
            return factory.random.randgen.randint(-2**16, 2**16)
        elif vr == VRs.ShortText:
            return factory.Faker('sentence').generate()
        elif vr == VRs.Time:
            return factory.Faker("dicom_time").generate({})
        elif vr == VRs.UniqueIdentifier:
            return factory.Faker("dicom_ui").generate({})
        elif vr == VRs.UnsignedLong:
            return factory.random.randgen.randint(0, 2**32)
        elif vr == VRs.Unknown:
            return "MockUnknown"
        elif vr == VRs.UnsignedShort:
            return factory.random.randgen.randint(0, 2**16)
        elif vr == VRs.UnlimitedText:
            return factory.Faker('text').generate()
        else:
            raise DataElementFactoryException(
                f"I dont know how to generate a mock value for"
                f" {vr}, the VR of '{self.tag}'")


class DataElementFactoryException(DICOMGeneratorException):
    pass