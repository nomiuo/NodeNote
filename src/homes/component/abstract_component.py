"""This module defines a standard that all components should follow.
"""

from abc import ABC
from typing import Optional

import PySide6
from PySide6.QtWidgets import QGraphicsWidget

from homes.component.layout.abstract_layout import AbstractLayout
from homes.model.persistence.serialization import Serialization


class AbstractComponent(QGraphicsWidget, Serialization, ABC):
    """This is the base component that any other component inherits from.

    Args:
        QGraphicsWidget (class): QGraphicsWidget inherits from QGraphicsLayoutItem.
        Serialization (class): Serialization interface.
        ABC (class): Abstract class.
    """

    def __init__(
        self,
        parent: Optional[PySide6.QtWidgets.QGraphicsItem] = ...,
        window_flags: PySide6.QtCore.Qt.WindowType = ...,
    ) -> None:
        """

        Args:
            parent (Optional[PySide6.QtWidgets.QGraphicsItem], optional): _description_. Defaults to ....
            window_flags (PySide6.QtCore.Qt.WindowType, optional): _description_. Defaults to ....
        """
        # Init.
        QGraphicsWidget.__init__(self, parent, window_flags)
        Serialization.__init__(self)

        # Container which could organize sub widgets.
        self.container: Optional[AbstractLayout] = None

        # Specific appearance which could be changed.
