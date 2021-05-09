from PyQt5 import QtGui, QtCore, QtWidgets
from Model.constants import *


__all__ = ["Pipe"]


class Pipe(QtWidgets.QGraphicsPathItem):
    def __init__(self, input_port=None, output_port=None, node=None):
        super(Pipe, self).__init__()
        self.node = node
        self.input_port = input_port
        self.output_port = output_port

        # BASIC SETTINGS
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
        self.setZValue(Z_VAL_PIPE)

        # DRAW PARAMETERS
        self.color = QtGui.QColor(0, 255, 204, 128)
        self.selected_color = QtGui.QColor(0, 153, 121, 255)

        # POS
        self.pos_source = self.node.get_port_position(self.input_port.port_type, self.input_port.port_truth)
        self.pos_destination = self.pos_source

    def paint(self, painter: QtGui.QPainter, option: QtWidgets.QStyleOptionGraphicsItem, widget=None) -> None:
        # DEFAULT PEN
        pen = QtGui.QPen(self.color if not self.isSelected() else self.selected_color)
        pen.setWidth(2)

        # DRAGGING PEN
        dragging_pen = QtGui.QPen(self.color)
        dragging_pen.setStyle(QtCore.Qt.DashLine)
        dragging_pen.setWidth(2)

        # PATH
        s = self.pos_source
        d = self.pos_destination
        dist = (d.x() - s.x()) * 0.5
        sspos = self.input_port.type
        s_x = +dist
        s_y = 0
        d_x = -dist
        d_y = 0

        if ((s.x() > d.x()) and sspos == OUTPUT_NODE_TYPE) or \
                ((s.x() < d.x()) and sspos == INPUT_NODE_TYPE):
            s_x *= -1  # > 0, s_y = 0  | < 0
            d_x *= -1  # < 0, d_y = 0  | > 0

        path = QtGui.QPainterPath(self.pos_source)
        path.cubicTo(
            s.x() + s_x, s.y() + s_y,  # CONTROL POINT
            d.x() + d_x, d.y() + d_y,  # CONTROL POINT
            d.x(), d.y()
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

    def update_position(self, pos_destination=None):
        self.pos_source = self.node.get_port_position(self.input_port.port_type, self.input_port.port_truth)
        if self.output_port is not None:
            self.pos_destination = self.output_port.parentItem().get_port_position(self.output_port.port_type, self.output_port.port_truth)
        elif pos_destination is not None:
            self.pos_destination = pos_destination
        else:
            self.pos_destination = self.pos_source
        self.update()
