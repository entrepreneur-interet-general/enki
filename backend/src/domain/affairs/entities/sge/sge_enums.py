from enum import Enum, auto


class SgeEnum(Enum):
    def __str__(self):
        return str(self.name)

    @classmethod
    def from_string(cls, value_string):
        return cls[value_string]


class SgeMessageTypeEnum(SgeEnum):
    Ack = auto()
    Report = auto()
    Error = auto()


class SgeEventType(SgeEnum):
    DISTRIBUTION_REUSSIE = auto()
    DISTRIBUTION_ERREUR = auto()
    RECEPTION_REUSSIE = auto()
    RECEPTION_ERREUR = auto()
    ROUTAGE_ERREUR = auto()
    ROUTAGE_REUSSI = auto()
