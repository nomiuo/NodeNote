"""This module defines a standard that all components should follow.
"""

from abc import ABC
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGraphicsItem, QGraphicsWidget


class AbstractComponent(QGraphicsWidget, ABC):
    """This is the base component that any other component inherits from.

    Args:
        QGraphicsWidget (class): public base class.
    """

    def __init__(
        self,
        parent: Optional[QGraphicsItem],
        wFlags: Qt.WindowFlags,
    ) -> None:
        """Init basic function.

        Args:
            parent (Optional[PySide6.QtWidgets.QGraphicsItem], optional):
                Parent widget.
            wFlags (PySide6.QtCore.Qt.WindowFlags, optional):
                Appearance window flags.
        """
        super().__init__(parent, wFlags)
