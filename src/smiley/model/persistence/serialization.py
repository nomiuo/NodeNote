"""This module has a serialization standard for all component.
"""

from abc import ABC, abstractmethod
from uuid import uuid1


class Serialization(ABC):
    """Every component must implement this serialization class."""

    def __init__(self):
        """Generate ramdom id.
        It should be noted that uuid1() depends on mac, timestamp,
        the probability of repetition is almost zero
        """
        self.__uuid = uuid1().hex

    @abstractmethod
    def serialize(self, serialization_object: object):
        """Serialize the object information into object.

        Args:
            serialization_object (object): Object of google protocol buffer.
        """

    @abstractmethod
    def deserialize(self, serialization_object: object):
        """Deserialize self by serialization object.

        Args:
            serialization_object (object): Object of google protocol buffer.
        """

    def get_uuid(self) -> str:
        """Get id of object which needs to be serialized.

        Returns:
            id (str): UUID of object.
        """
        return self.__uuid
