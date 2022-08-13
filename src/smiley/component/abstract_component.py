"""This module defines a standard that all components should follow.
"""

from abc import ABC
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGraphicsItem, QGraphicsWidget

from smiley.component.layout.abstract_layout import AbstractLayout
from smiley.model.persistence.serialization import Serialization


class AbstractComponent(QGraphicsWidget, Serialization, ABC):
    """This is the base component that any other component inherits from.

    Args:
        QGraphicsWidget (class): QGraphicsWidget inherits from QGraphicsLayoutItem.
        Serialization (class): Serialization interface.
        ABC (class): Abstract class.
    """

    def __init__(
        self,
        parent: Optional[QGraphicsItem],
        wFlags: Qt.WindowFlags,
    ) -> None:
        # Init.
        QGraphicsWidget.__init__(self, parent, wFlags)
        Serialization.__init__(self)

        # Container which could organize sub widgets.
        self.container: Optional[AbstractLayout] = None

        # Specific appearance which could be changed.
