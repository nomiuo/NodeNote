"""This module defines a standard effect of mouse event.
"""


from abc import ABC, abstractmethod

from PySide6 import QtWidgets


class AbstractMouseEffect(ABC):
    """Some abstract mouse effect method which should be implemented.

    - click_effect: When user clicks this item, effect will show.
    - double_click_effect: When user double clicks this item, effect will show.
    - hover_effect: When mouse hovers over this item, effect will show.

    Args:
        ABC (class): Abstract class.
    """

    @staticmethod
    @abstractmethod
    def click_effect(
        target: QtWidgets.QGraphicsWidget,
        event: QtWidgets.QGraphicsSceneMouseEvent,
    ) -> None:
        """Add effect into click event

        Args:
            target (QtWidgets.QGraphicsWidget): Target QGraphicsWidget.
            event (QtWidgets.QGraphicsSceneMouseEvent): MouseClickEvent.
        """

    @staticmethod
    @abstractmethod
    def double_click_effect(
        target: QtWidgets.QGraphicsWidget,
        event: QtWidgets.QGraphicsSceneMouseEvent,
    ) -> None:
        """Add effect into double click event.

        Args:
            target (QtWidgets.QGraphicsWidget): Target QGraphicsWidget.
            event (QtWidgets.QGraphicsSceneMouseEvent): MouseDoubleClickEvent.
        """

    @staticmethod
    @abstractmethod
    def hover_effect(
        target: QtWidgets.QGraphicsWidget,
        event: QtWidgets.QGraphicsSceneMouseEvent,
    ) -> None:
        """Add effect into mouse hover event.

        Args:
            target (QtWidgets.QGraphicsWidget): Target QGraphicsWidget.
            event (QtWidgets.QGraphicsSceneMouseEvent): MouseHoverEvent.
        """
