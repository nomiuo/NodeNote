from enum import Enum, auto

from homes.constant.enum.abstract_enum import AbstractEnum

__all__ = ["AppearanceLevel"]


class AppearanceLevel(AbstractEnum):
    class Level(Enum):
        GLOBAL = auto()
        SCENE = auto()
        KIND = auto()
        GROUP = auto()
        SPECIFIC = auto()

    def serialize(self, serialization_object: object):
        return super().serialize(serialization_object)

    def deserialize(self, serialization_object: object):
        return super().deserialize(serialization_object)
