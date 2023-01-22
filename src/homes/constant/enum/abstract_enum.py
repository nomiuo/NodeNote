"""This module define an abstract interface for enum.

Every enum must implement serialization interface and
it provides setting level ability.
"""

from enum import Enum
from typing import Dict, Type

from homes.constant.constant import OK, ORDER_WRONG
from homes.model.persistence.serialization import Serialization

__all__ = ["AbstractEnum"]


class AbstractEnum(Serialization):
    """Abstract enum must be inherited by Enum class.

    Every class inherited from AbstractEnum could set
    oder attribute of enum just because of the immutable
    attribute of element of enum. It works by serializing
    enum into dict.

    Args:
        Serialization (class): Serialization interface.
    """

    DICT: Dict[Enum, int] = {}

    def __init__(self, enum: Type[Enum]):
        """Serialize enum into dict.

        Args:
            enum (Type[Enum]): Enum.
        """
        super().__init__()

        # Serialize enum into dict.
        order = 0
        for ele in enum:
            self.DICT[ele] = order
            order += 1

    def set_order(self, name: Enum, order: int) -> str:
        """Set the order of enum.

        It should be noted that the order passed by user
        can not be same as other oder because the order
        will be used as level.

        Args:
            name (Enum): Element of enum which should be \
                in Enum.
            order (int): Level of element which should be \
                greater than or equal to zero.

        Returns:
            str: Return OK or other wrong message.
        """
        # For security.
        assert order >= 0

        # Determine whether name is in the dictionary.
        assert name in self.DICT

        # Set the correct order.
        if order in self.DICT.values():
            return ORDER_WRONG
        self.DICT[name] = order

        return OK

    def get_order(self, name: Enum) -> int:
        """Get the order of the specific enum.

        Args:
            name (Enum): The enum.

        Returns:
            int: Return order if ok, else return -1.
        """
        if name not in self.DICT:
            return -1
        return self.DICT[name]
