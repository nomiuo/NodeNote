from abc import ABC, abstractmethod
from typing import Union

import PySide6
from PySide6.QtWidgets import QGraphicsLayout

__all__ = ["AbstractLayout"]


class AbstractLayout(QGraphicsLayout, ABC):
    @abstractmethod
    def setGeometry(
        self, rect: Union[PySide6.QtCore.QRectF, PySide6.QtCore.QRect]
    ) -> None:
        return super().setGeometry(rect)

    @abstractmethod
    def sizeHint(  # type: ignore
        self,
        which: PySide6.QtCore.Qt.SizeHint,
        constraint: Union[PySide6.QtCore.QSizeF, PySide6.QtCore.QSize],
    ) -> PySide6.QtCore.QSizeF:
        return super().sizeHint(which, constraint)

    @abstractmethod
    def count(self) -> int:
        return super().count()

    @abstractmethod
    def itemAt(self, i: int) -> PySide6.QtWidgets.QGraphicsLayoutItem:
        return super().itemAt(i)

    @abstractmethod
    def removeAt(self, index: int) -> None:
        return super().removeAt(index)
