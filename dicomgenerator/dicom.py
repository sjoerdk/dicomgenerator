"""Definitions from the DICOM world
"""


class VR:
    """A DICOM Value representation (data type)

    Made this because I can never remember the short name strings.
    """
    def __init__(self, short_name, long_name):
        self.short_name = short_name
        self.long_name = long_name

    def __str__(self):
        return f'VR "{self.long_name}" ({self.short_name})'


class VRs:
    """ All value representations listed here:

    http://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.2.html
    """
    ApplicationEntity = VR(short_name='AE', long_name='Application Entity')
    AgeString = VR(short_name='AS', long_name='Age String')
    AttributeTag = VR(short_name='AT', long_name='Attribute Tag')
    CodeString = VR(short_name='CS', long_name='Code String')
    Date = VR(short_name='DA', long_name='Date')
    DecimalString = VR(short_name='DS', long_name='Decimal String')
    DateTime = VR(short_name='DT', long_name='Date Time')
    FloatingPointSingle = VR(short_name='FL', long_name='Floating Point Single')
    FloatingPointDouble = VR(short_name='FD', long_name='Floating Point Double')
    IntegerString = VR(short_name='IS', long_name='Integer String')
    LongString = VR(short_name='LO', long_name='Long String')
    LongText = VR(short_name='LT', long_name='Long Text')
    OtherByteString = VR(short_name='OB', long_name='Other Byte String')
    OtherDoubleString = VR(short_name='OD', long_name='Other Double String')
    OtherFloatString = VR(short_name='OF', long_name='Other Float String')
    OtherWordString = VR(short_name='OW', long_name='Other Word String')
    PersonName = VR(short_name='PN', long_name='Person Name')
    ShortString = VR(short_name='SH', long_name='Short String')
    SignedLong = VR(short_name='SL', long_name='Signed Long')
    Sequence = VR(short_name='SQ', long_name='Sequence of Items')
    SignedShort = VR(short_name='SS', long_name='Signed Short')
    ShortText = VR(short_name='ST', long_name='Short Text')
    Time = VR(short_name='TM', long_name='Time')
    UniqueIdentifier = VR(short_name='UI', long_name='Unique Identifier (UID)')
    UnsignedLong = VR(short_name='UL', long_name='Unsigned Long')
    Unknown = VR(short_name='UN', long_name='Unknown')
    UnsignedShort = VR(short_name='US', long_name='Unsigned Short')
    UnlimitedText = VR(short_name='UT', long_name='Unlimited Text')

    all = [ApplicationEntity, AgeString, AttributeTag, CodeString, Date,
           DecimalString, DateTime, FloatingPointSingle, FloatingPointDouble,
           IntegerString, LongString, LongText, OtherByteString, OtherDoubleString,
           OtherFloatString, OtherWordString, PersonName, ShortString, SignedLong,
           Sequence, SignedShort, ShortText, Time, UniqueIdentifier, UnsignedLong,
           Unknown, UnsignedShort, UnlimitedText]

    by_short_name = {x.short_name: x for x in all}

    # VRs which could reasonably have random string contents
    string_like = [LongString, LongText, PersonName, ShortString, ShortText,
                   UniqueIdentifier, UnlimitedText]

    # VRs which represent numbers
    numeric = [DecimalString, FloatingPointDouble, FloatingPointDouble, IntegerString,
               OtherDoubleString, OtherFloatString, SignedLong, SignedShort,
               UnsignedShort, UnsignedLong]

    # VRs which represent dates and times
    date_like = [Date, DateTime, Time]

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
        except KeyError:
            raise ValueError(f"Unknown VR '{short_name}'")
