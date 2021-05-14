from PyQt5 import QtWidgets, QtGui, QtCore
from Model import constants


class Container(QtWidgets.QGraphicsItem):
    def __init__(self, parent=None):
        super(Container, self).__init__(parent)
        self.line_points = []
        self.pen = QtGui.QPen(QtGui.QColor(255, 128, 128, 200), 2)
        self.pen.setDashPattern([3, 3])
        self.setZValue(constants.Z_VAL_CONTAINERS)

    def boundingRect(self) -> QtCore.QRectF:
        return QtCore.QRectF(0, 0, 1, 1)

    def paint(self, painter, option, widget=None) -> None:
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.setPen(self.pen)

        poly = QtGui.QPolygonF(self.line_points)
        painter.drawPolyline(poly)
