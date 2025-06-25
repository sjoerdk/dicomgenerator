"""General functions to create pydicom datasets"""

import datetime
import factory
import json
import pydicom

from pydicom.datadict import dictionary_VR
from pydicom.dataset import Dataset
from pydicom.tag import Tag

from dicomgenerator.dicom import VRs
from dicomgenerator.exceptions import DICOMGeneratorError
from dicomgenerator.settings import DICOM_GENERATOR_ROOT_UID
from factory.fuzzy import FuzzyDate
from faker.providers import BaseProvider
from faker import Faker
from pydicom.uid import generate_uid


def quick_dataset(*_, **kwargs) -> Dataset:
    """A dataset with keyword args as tagname - value pairs

    For example:
    >>> ds = quick_dataset(PatientName='Jane', StudyDescription='Test')
    >>> ds.PatientName
    'Jane'
    >>> ds.StudyDescription
    'Test'

    Raises
    ------
    ValueError
        If any input key is not a valid DICOM keyword

    """
    dataset = Dataset()
    for tagname, value in kwargs.items():
        Tag(tagname)  # assert valid dicom keyword. pydicom will not do this.
        dataset.__setattr__(tagname, value)
    return dataset


class FuzzyDICOMDateString(FuzzyDate):
    """A valid DICOM value for a DA (Date) type value

    see
    http://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.2.html
    """

    def fuzz(self):
        date = super().fuzz()
        return date.strftime("%Y%m%d")


class DatasetFactory(factory.Factory):
    """Generates a pydicom dataset based on a json-dicom template"""

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
            *args,
            json_dataset=json.load(open(template_path)),
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
        """Something like 'DoeFake^Jane' or 'VriesFake^Sep de' (VR = PN)

        Prepending 'Fake' to make fake names easily recognisable. This avoids
        situations in which real names are mistaken for fake names.

        Returns
        -------
        str
        """
        faker = Faker(locale=self.locale)
        return f"{faker.last_name()}Test^{faker.first_name()}"

    @staticmethod
    def dicom_time():
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

    @staticmethod
    def dicom_date():
        """Dicom date string. Like 20120425 (VR = DA)

        Returns
        -------
        str
        """
        date = FuzzyDate(
            start_date=datetime.date(2008, 1, 1), end_date=datetime.date(2013, 4, 16)
        ).fuzz()
        return date.strftime("%Y%m%d")

    @staticmethod
    def dicom_ui():
        """Generate Valid DICOM UID (VR = UI)

        Uses factory boy random seed, so setting seed in test yields the same
        UID value each time

        Returns
        -------
        str
        """
        return str(
            generate_uid(
                prefix=DICOM_GENERATOR_ROOT_UID,
                entropy_srcs=[str(factory.random.randgen.getrandbits(100))],
            ),
        )


factory.Faker.add_provider(DICOMVRProvider)


class DataElementFactory(factory.Factory):
    """Generates pydicom DataElements.

    Will always match VR and random value to given values

    >>> DataElementFactory(tag='PatientName').VR = 'PN'
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

    tag = Tag("PatientID")

    @factory.lazy_attribute
    def VR(self):  # noqa This has to uppercase to match pydicom DataElement
        """Find the correct Value Representation for this tag from pydicom"""
        try:
            return dictionary_VR(Tag(self.tag))
        except KeyError:
            # unknown tag. Just return set value, assuming user want to just
            # get on with it
            return VRs.LongString.short_name

    @factory.lazy_attribute
    def value(self):  # noqa
        """Generate a valid mock value for this type of VR

        Raises
        ------
        DataElementFactoryException
            If a value cannot be generated
        """
        faker = Faker()
        faker.add_provider(DICOMVRProvider)
        vr = VRs.short_name_to_vr(self.VR)
        if vr == VRs.ApplicationEntity:
            return "MockEntity"
        elif vr == VRs.AgeString:
            return f"{factory.random.randgen.randint(0, 120): 03d}Y"
        elif vr == VRs.AttributeTag:
            return 0x0010, 0x0010
        elif vr == VRs.CodeString:
            return "MOCK_123_CODE"
        elif vr == VRs.Date:
            return faker.dicom_date()
        elif vr == VRs.DecimalString:
            return "+10.4"
        elif vr == VRs.DateTime:
            return faker.dicom_date() + faker.dicom_time()
        elif vr == VRs.FloatingPointSingle:
            return 1.1
        elif vr == VRs.FloatingPointDouble:
            return 1.123
        elif vr == VRs.IntegerString:
            return f"{factory.random.randgen.randint(-2**31, 2**31)}"
        elif vr == VRs.LongString:
            return faker.sentence()[:64]
        elif vr == VRs.LongText:
            return faker.text()[:10240]
        elif vr == VRs.OtherByteString:
            return b"\x13\00"
        elif vr == VRs.OtherDoubleString:
            return "MockDoubleString"
        elif vr == VRs.OtherFloatString:
            return "MockFloatString"
        elif vr == VRs.OtherWordString:
            return b"MockOtherWordString"
        elif vr == VRs.PersonName:
            return faker.dicom_person_name()
        elif vr == VRs.ShortString:
            return "MockShortString"
        elif vr == VRs.SignedLong:
            return factory.random.randgen.randint(-(2**31), 2**31)
        elif vr == VRs.Sequence:
            return []
        elif vr == VRs.SignedShort:
            return factory.random.randgen.randint(-(2**15), 2**15)
        elif vr == VRs.ShortText:
            return faker.sentence()
        elif vr == VRs.Time:
            return faker.dicom_time()
        elif vr == VRs.UniqueIdentifier:
            return faker.dicom_ui()
        elif vr == VRs.UnsignedLong:
            return factory.random.randgen.randint(0, 2**31)
        elif vr == VRs.Unknown:
            return "MockUnknown"
        elif vr == VRs.UnsignedShort:
            return factory.random.randgen.randint(0, 2**15)
        elif vr == VRs.UnlimitedText:
            return faker.text()
        else:
            raise DataElementFactoryError(
                f"I dont know how to generate a mock value for"
                f" {vr}, the VR of '{self.tag}'"
            )


class DataElementFactoryError(DICOMGeneratorError):
    pass
