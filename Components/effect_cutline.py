from PyQt5 import QtWidgets, QtGui, QtCore
from Model import constants


class EffectCutline(QtWidgets.QGraphicsItem):
    def __init__(self, parent=None):
        super(EffectCutline, self).__init__(parent)
        self.line_points = []
        self.pen = QtGui.QPen(QtCore.Qt.white, 2)
        self.pen.setDashPattern([3, 3])
        self.setZValue(constants.Z_VAL_CUTLINE)

    def boundingRect(self) -> QtCore.QRectF:
        return QtCore.QRectF(0, 0, 1, 1)

    def paint(self, painter, option, widget=None) -> None:
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.setPen(self.pen)

        poly = QtGui.QPolygonF(self.line_points)
        painter.drawPolyline(poly)
