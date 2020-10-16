from abc import ABC


class Entity(ABC):
    uuid: str

    def __eq__(self, other):
        return self.uuid == other.uuid
