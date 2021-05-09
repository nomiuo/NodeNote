from PyQt5 import QtWidgets, QtGui, QtCore


__all__ = ["Scene"]


class Scene(QtWidgets.QGraphicsScene):
    def __init__(self, view, parent=None):
        super(Scene, self).__init__(parent)
        self.view = view
        self.scene_width = 1080
        self.scene_height = 900
        self.setSceneRect(QtCore.QRectF(0, 0, self.scene_width, self.scene_height))
