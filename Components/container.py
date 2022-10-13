from collections import OrderedDict
from PyQt5 import QtWidgets, QtGui, QtCore
from Model import constants, serializable


class Container(QtWidgets.QGraphicsPathItem, serializable.Serializable):
    width = 4
    color = QtGui.QColor(255, 128, 128, 255)
    selected_color = QtGui.QColor(128, 0, 0, 128)

    def __init__(self, pos, parent=None):
        super(Container, self).__init__(parent)
        self.start_point = pos
        self.next_point = QtCore.QPointF()
        self.points = list()
        self.points.append((pos.x(), pos.y()))
        self.draw_path = QtGui.QPainterPath(self.start_point)

        self.pen = QtGui.QPen(self.color, self.width)
        self.pen.setDashPattern([1, 1])
        self.selected_pen = QtGui.QPen(self.selected_color, self.width)

        self.setZValue(constants.Z_VAL_CONTAINERS)
        self.setFlags(QtWidgets.QGraphicsItem.ItemIsMovable | QtWidgets.QGraphicsItem.ItemIsSelectable)

        self.deserialize_flag = False

        # Style
        self.width_flag = False
        self.color_flag = False
        self.selected_color_flag = False

    def paint(self, painter, option, widget=None) -> None:
        #   Width and color init
        if self.scene().container_style_width and not self.width_flag:
            self.width = self.scene().container_style_width
        if self.scene().container_style_color and not self.color_flag:
            self.color = self.scene().container_style_selected_color
        if self.scene().container_style_selected_color and not self.selected_color_flag:
            self.selected_color = self.scene().container_style_selected_color

        self.pen = QtGui.QPen(self.color, self.width)
        self.pen.setDashPattern([1, 1])
        self.selected_pen = QtGui.QPen(self.selected_color, self.width)

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
            self.deserialize_flag = False

    def serialize(self):
        return OrderedDict([
            ('id', self.id),
            ('points', self.points),
            ('width', self.width),
            ('color', self.color.rgba()),
            ('selected color', self.selected_color.rgba()),
            ('width flag', self.width_flag),
            ('color flag', self.color_flag),
            ('selected color flag', self.selected_color_flag)
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
        # style
        self.width = data['width']

        self.color = QtGui.QColor()
        self.color.setRgba(data['color'])

        self.selected_color = QtGui.QColor()
        self.selected_color.setRgba(data['selected color'])

        # flag
        self.width_flag = data['width flag']
        self.color_flag = data['color flag']
        self.selected_color_flag = data['selected color flag']

        return True
