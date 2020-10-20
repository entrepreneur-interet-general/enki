from enum import Enum


class CisuEnum(Enum):
    def __str__(self):
        return str(self.name)

    @classmethod
    def from_string(cls, value_string):
        return cls[value_string]
