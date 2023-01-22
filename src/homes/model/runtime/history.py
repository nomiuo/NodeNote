from typing import Final, List

from homes.model.runtime.abstract_operation import AbstractOperation


class History:
    # Operations that user did.
    __operations: List[AbstractOperation] = []

    # The __point points the last operation user did.
    __point: int = -1

    # The maximum recoverable number.
    __MAX_OPERATIONS: Final[int] = 500

    def add_operation(self, operation: AbstractOperation):
        """Every time user did an operation, call this function.

        Args:
            operation (AbstractOperation): The operation user did.
        """
        self.__operations.append(operation)
        self.__point += 1

    def remove_operation(self):
        # For security
        assert self.__point - 1 >= -1

        # Move point forward one index.
        self.__point -= 1

    def undo(self):
        """Undo the last operation."""
        # Can not undo because of no enough operation.
        if self.__point == -1:
            return

        self.__operations[self.__point].undo()

    def redo(self):
        """Redo the next operation."""
