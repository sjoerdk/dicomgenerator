"""Definitions from the DICOM world"""


class VR:
    """A DICOM Value representation (data type).

    Made this because I can never remember the short name strings.
    """

    def __init__(self, short_name, long_name):
        self.short_name = short_name
        self.long_name = long_name

    def __str__(self):
        return f'VR "{self.long_name}" ({self.short_name})'


class StringLikeVR(VR):
    pass


class DateLikeVR(VR):
    pass


class NumericVR(VR):
    pass


class BytesLikeVR(VR):
    pass


class VRs:
    """All value representations listed here:

    http://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.2.html
    """

    ApplicationEntity = VR(short_name="AE", long_name="Application Entity")
    AgeString = VR(short_name="AS", long_name="Age String")
    AttributeTag = VR(short_name="AT", long_name="Attribute Tag")
    CodeString = StringLikeVR(short_name="CS", long_name="Code String")
    Date = DateLikeVR(short_name="DA", long_name="Date")
    DecimalString = NumericVR(short_name="DS", long_name="Decimal String")
    DateTime = DateLikeVR(short_name="DT", long_name="Date Time")
    FloatingPointSingle = NumericVR(short_name="FL", long_name="Floating Point Single")
    FloatingPointDouble = NumericVR(short_name="FD", long_name="Floating Point Double")
    IntegerString = NumericVR(short_name="IS", long_name="Integer String")
    LongString = StringLikeVR(short_name="LO", long_name="Long String")
    LongText = StringLikeVR(short_name="LT", long_name="Long Text")
    OtherByteString = BytesLikeVR(short_name="OB", long_name="Other Byte String")
    OtherDoubleString = NumericVR(short_name="OD", long_name="Other Double String")
    OtherFloatString = NumericVR(short_name="OF", long_name="Other Float String")
    OtherWordString = BytesLikeVR(short_name="OW", long_name="Other Word String")
    PersonName = StringLikeVR(short_name="PN", long_name="Person Name")
    ShortString = StringLikeVR(short_name="SH", long_name="Short String")
    SignedLong = NumericVR(short_name="SL", long_name="Signed Long")
    Sequence = VR(short_name="SQ", long_name="Sequence of Items")
    SignedShort = NumericVR(short_name="SS", long_name="Signed Short")
    ShortText = StringLikeVR(short_name="ST", long_name="Short Text")
    Time = DateLikeVR(short_name="TM", long_name="Time")
    UniqueIdentifier = StringLikeVR(
        short_name="UI", long_name="Unique Identifier (UID)"
    )
    UnsignedLong = NumericVR(short_name="UL", long_name="Unsigned Long")
    Unknown = VR(short_name="UN", long_name="Unknown")
    UnsignedShort = NumericVR(short_name="US", long_name="Unsigned Short")
    UnlimitedText = StringLikeVR(short_name="UT", long_name="Unlimited Text")

    all = [
        ApplicationEntity,
        AgeString,
        AttributeTag,
        CodeString,
        Date,
        DecimalString,
        DateTime,
        FloatingPointSingle,
        FloatingPointDouble,
        IntegerString,
        LongString,
        LongText,
        OtherByteString,
        OtherDoubleString,
        OtherFloatString,
        OtherWordString,
        PersonName,
        ShortString,
        SignedLong,
        Sequence,
        SignedShort,
        ShortText,
        Time,
        UniqueIdentifier,
        UnsignedLong,
        Unknown,
        UnsignedShort,
        UnlimitedText,
    ]

    by_short_name = {x.short_name: x for x in all}

    @classmethod
    def short_name_to_vr(cls, short_name) -> VR:
        """Find a VR with the given short name

        Raises
        ------
        ValueError
            When no VR object can be found with the given short name
        """
        try:
            return cls.by_short_name[short_name]
        except KeyError as e:
            raise ValueError(f"Unknown VR '{short_name}'") from e

    @classmethod
    def is_date_like(cls, vr: str) -> bool:
        """Is the given VR like a date or time?"""
        return isinstance(cls.short_name_to_vr(vr), DateLikeVR)

    @classmethod
    def is_string_like(cls, vr: str) -> bool:
        """Is the given VR like a string?"""
        return isinstance(cls.short_name_to_vr(vr), StringLikeVR)

    @classmethod
    def is_numeric(cls, vr: str) -> bool:
        """Is the given VR like a number?"""
        return isinstance(cls.short_name_to_vr(vr), NumericVR)

    @classmethod
    def is_bytes_like(cls, vr: str) -> bool:
        """Is the given VR like a number?"""
        return isinstance(cls.short_name_to_vr(vr), BytesLikeVR)

    @classmethod
    def is_sequence(cls, vr: str) -> bool:
        """Is the given VR a sequence of elements?"""
        return bool(vr == cls.Sequence.short_name)
