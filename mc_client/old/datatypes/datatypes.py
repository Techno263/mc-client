from enum import IntEnum

class DatatypeSize(IntEnum):
    Boolean = 1
    SByte = 1
    Byte = 1
    Short = 2
    UShort = 2
    Int = 4
    Long = 8
    Float = 4
    Double = 8
    Position = 8
    Angle = 1
    UUID = 16
