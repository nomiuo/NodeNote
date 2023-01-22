"""This module defines an interface for all operations."""

from abc import ABC, abstractmethod
from typing import Any


class AbstractOperation(ABC):
    """Interface for every operation.

    Every operation must implement undo&&redo
    function.

    To instantiate this class, user should provide
    the operation done.

    Args:
        ABC (class): Abstract class.
    """

    __operation: Any = None

    def __init__(self, operation: Any) -> None:
        super().__init__()

        self.__operation = operation

    @staticmethod
    @abstractmethod
    def undo():
        """Undo operation through different `__operation`.

        Raises:
            NotImplementedError: Abstract interface.
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def redo():
        """Redo operation through different `__operation`.

        Raises:
            NotImplementedError: Abstract interface.
        """
        raise NotImplementedError

    def get_operation(self) -> Any:
        """Get the operation.

        Returns:
            Any: Operation.
        """
        return self.__operation
