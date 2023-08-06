from enum import Enum


class Metadata(str, Enum):
    IP_ADDRESS: str = "x-forwarded-for"
    USER_AGENT: str = "x-user-agent"
