from collections import OrderedDict
from PyQt5 import QtWidgets, QtGui, QtCore
from Model import constants, serializable


class Container(QtWidgets.QGraphicsPathItem, serializable.Serializable):
    def __init__(self, pos, parent=None):
        super(Container, self).__init__(parent)
        self.start_point = pos
        self.next_point = QtCore.QPointF()
        self.points = list()
        self.points.append((pos.x(), pos.y()))
        self.draw_path = QtGui.QPainterPath(self.start_point)

        self.pen = QtGui.QPen(QtGui.QColor(255, 128, 128, 255))
        self.pen.setDashPattern([1, 1])
        self.selected_pen = QtGui.QPen(QtGui.QColor(128, 0, 0, 128))

        self.setZValue(constants.Z_VAL_CONTAINERS)
        self.setFlags(QtWidgets.QGraphicsItem.ItemIsMovable | QtWidgets.QGraphicsItem.ItemIsSelectable)

        self.deserialize_flag = False

    def paint(self, painter, option, widget=None) -> None:
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.setPen(self.pen if not self.isSelected() else self.selected_pen)

        if not self.deserialize_flag:
            if self.next_point:
                self.points.append((self.next_point.x(), self.next_point.y()))
                self.draw_path.lineTo(self.next_point)
                self.draw_path.moveTo(self.next_point)
            self.setPath(self.draw_path)
            painter.drawPath(self.path())
        else:
            for point in self.points:
                self.draw_path.lineTo(QtCore.QPointF(point[0], point[1]))
                self.draw_path.moveTo(QtCore.QPointF(point[0], point[1]))
            self.setPath(self.draw_path)
            painter.drawPath(self.path())

    def serialize(self):
        return OrderedDict([
            ('id', self.id),
            ('points', self.points)
        ])

    def deserialize(self, data, hashmap: dict, view=None, flag=True):
        # added into scene and view
        view.current_scene.addItem(self)
        view.containers.append(self)
        # id
        self.id = data['id']
        # draw point
        self.points = data['points']
        self.deserialize_flag = True
        return True
