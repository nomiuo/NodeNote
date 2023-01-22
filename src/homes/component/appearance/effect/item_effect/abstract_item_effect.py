"""This module defines a standard effect of item.
"""


from abc import ABC, abstractmethod

from PySide6 import QtWidgets


class AbstractItemEffect(ABC):
    """Some abstract item effect method which should be implemented.

    - move_effect: When item is moving, effect will show.
    - create_effect: When item is created, effect will show.
    - delete_effect: When item is deleted, effect will show.

    Args:
        ABC (class): Abstract class.
    """

    @staticmethod
    @abstractmethod
    def move_effect(
        target: QtWidgets.QGraphicsWidget,
        event: QtWidgets.QGraphicsSceneMoveEvent,
    ) -> None:
        """Move item with specific effect.

        Args:
            target (QtWidgets.QGraphicsWidget): Target widget.
            event (QtWidgets.QGraphicsSceneMoveEvent): Move event.
        """

    @staticmethod
    @abstractmethod
    def create_effect(
        target: QtWidgets.QGraphicsWidget,
    ) -> None:
        """Create item with specific effect.

        Args:
            target (QtWidgets.QGraphicsWidget): Target widget.
        """

    @staticmethod
    @abstractmethod
    def delete_effect(
        target: QtWidgets.QGraphicsWidget,
    ) -> None:
        """Delete item with specific effect.

        Args:
            target (QtWidgets.QGraphicsWidget): Target widget.
        """
