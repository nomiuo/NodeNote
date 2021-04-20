from PyQt5 import QtGui, QtCore, QtWidgets
from Model.constants import *


__all__ = ["Pipe"]


class Pipe(QtWidgets.QGraphicsPathItem):
    def __init__(self, input_port=None, output_port=None, parent=None):
        super(Pipe, self).__init__(parent)
        self.node = parent
        # BASIC SETTINGS
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
        self.setZValue(Z_VAL_PORT)

        # DRAW PARAMETERS
        self.color = QtGui.QColor(0, 255, 204, 128)
        self.selected_color = QtGui.QColor(0, 153, 121, 255)

        # POS
        self.posSource = [0, 0]
        self.posDestination = [200, 100]

        # PORT
        self.input_port = input_port
        self.output_port = output_port

    def paint(self, painter: QtGui.QPainter, option: QtWidgets.QStyleOptionGraphicsItem, widget=None) -> None:
        # DEFAULT PEN
        pen = QtGui.QPen(self.color if not self.isSelected() else self.selected_color)
        pen.setWidth(2)

        # DRAGGING PEN
        dragging_pen = QtGui.QPen(self.color)
        dragging_pen.setStyle(QtCore.Qt.DashLine)
        dragging_pen.setWidth(2)

        # PATH
        s = self.posSource
        d = self.posDestination
        dist = (d[0] - s[0]) * 0.5
        sspos = self.input_port.type
        s_x = +dist
        s_y = 0
        d_x = -dist
        d_y = 0

        if ((s[0] > d[0]) and sspos == OUTPUT_NODE_TYPE) or \
                ((s[0] < d[0]) and sspos == INPUT_NODE_TYPE):
            s_x *= -1  # > 0, s_y = 0  | < 0
            d_x *= -1  # < 0, d_y = 0  | > 0

        path = QtGui.QPainterPath(QtCore.QPointF(*self.posSource))
        path.cubicTo(
            s[0] + s_x, s[1] + s_y,  # CONTROL POINT
            d[0] + d_x, d[1] + d_y,  # CONTROL POINT
            d[0], d[1]
        )
        self.setPath(path)

        # PEN
        if self.output_port is None:
            painter.setPen(dragging_pen)
        else:
            painter.setPen(pen)

        # DRAW
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawPath(self.path())

    def update_position(self):
        source_pos = self.node.get_port_position(INPUT_NODE_TYPE)
        source_pos[0] += self.node.pos().x()
        source_pos[1] += self.node.pos().y()
        self.posSource = source_pos

        if self.output_port is not None:
            destination_pos = self.node.get_port_position(OUTPUT_NODE_TYPE)
            destination_pos[0] += self.node.pos().x()
            destination_pos[1] += self.node.pos().y()
        else:
            self.posDestination = source_pos
        self.update()
