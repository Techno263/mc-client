from enum import IntEnum

class PacketID(IntEnum):
    LoginStart = 0x00
    EncryptionResponse = 0x01
    LoginPluginResponse = 0x02
