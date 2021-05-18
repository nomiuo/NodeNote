from collections import OrderedDict
from PyQt5 import QtWidgets, QtGui, QtCore
from Model import constants, serializable


class Container(QtWidgets.QGraphicsPathItem, serializable.Serializable):
    def __init__(self, pos, parent=None):
        super(Container, self).__init__(parent)
        self.start_point = pos
        self.next_point = QtCore.QPointF()
        self.draw_path = QtGui.QPainterPath(self.start_point)

        self.pen = QtGui.QPen(QtGui.QColor(255, 128, 128, 255))
        self.pen.setDashPattern([1, 1])
        self.selected_pen = QtGui.QPen(QtGui.QColor(128, 0, 0, 128))

        self.setZValue(constants.Z_VAL_CONTAINERS)
        self.setFlags(QtWidgets.QGraphicsItem.ItemIsMovable | QtWidgets.QGraphicsItem.ItemIsSelectable)

    def paint(self, painter, option, widget=None) -> None:
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.setPen(self.pen if not self.isSelected() else self.selected_pen)

        if self.next_point:
            self.draw_path.lineTo(self.next_point)
            self.draw_path.moveTo(self.next_point)
        self.setPath(self.draw_path)
        painter.drawPath(self.path())

    def serialize(self):
        return OrderedDict([
            ('id', self.id),
            ('path', id(self.draw_path))
        ])
