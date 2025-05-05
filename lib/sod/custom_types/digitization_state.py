from enum import Enum


class DigitizationState(Enum):
    Finished = "Finished"
    InProgress = "InProgress"
    Planned = "Planned"
    Revision = "Revision"
    Unknown = "Unknown"
    NotDigitized = "NotDigitized"
