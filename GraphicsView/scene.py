from PyQt5 import QtWidgets, QtGui, QtCore


__all__ = ["Scene"]


class Scene(QtWidgets.QGraphicsScene):
    def __init__(self, view, parent=None):
        super(Scene, self).__init__(parent)
        self.view = view
        self.setSceneRect(QtCore.QRectF())
