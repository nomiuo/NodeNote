from PyQt5 import QtGui, QtCore, QtWidgets
from Model.constants import *
from Components import attribute

__all__ = ["Pipe"]


class Pipe(QtWidgets.QGraphicsPathItem):
    def __init__(self, input_port=None, output_port=None, node=None):
        super(Pipe, self).__init__()
        self.node = node
        self.start_port = input_port
        self.end_port = output_port

        # BASIC SETTINGS
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
        self.setZValue(Z_VAL_PIPE)

        # DRAW PARAMETERS
        self.color = QtGui.QColor(0, 255, 204, 128)
        self.selected_color = QtGui.QColor(0, 153, 121, 255)

        # POS
        self.pos_source = self.node.get_port_position(self.start_port.port_type, self.start_port.port_truth)
        self.pos_destination = self.pos_source

        # ANIMATION
        self.timeline = QtCore.QTimeLine(2000)
        self.timeline.frameChanged.connect(self.timeline_frame_changed)
        self.timeline.setLoopCount(0)

        ellips_size = QtCore.QRectF(-5, -5, 10, 10)
        ellips_color = QtGui.QColor(255, 153, 153, 200)
        ellips_thickness = 2
        ellips_pen = QtGui.QPen(ellips_color, ellips_thickness, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap,
                                QtCore.Qt.RoundJoin)
        self.ellips_item = QtWidgets.QGraphicsEllipseItem(ellips_size, self)
        self.ellips_item.setBrush(ellips_color)
        self.ellips_item.setPen(ellips_pen)
        if input_port.port_type == OUTPUT_NODE_TYPE:
            self.ellips_item.setPos(self.path().pointAtPercent(0.0))
            self.timeline.setFrameRange(0, 100)
        else:
            self.ellips_item.setPos(self.path().pointAtPercent(1))
            self.timeline.setFrameRange(100, 0)
        self.ellips_item.hide()

        # EDIT
        self.edit = attribute.SimpleTextField("Deafult", self)
        self.edit.setFont(QtGui.QFont("LucidaMacBold", 8))
        bound_rect_width, bound_rect_height = self.edit.boundingRect().width(), self.edit.boundingRect().height()
        self.edit.setPos(self.path().pointAtPercent(0.5).x() - (bound_rect_width // 2),
                         self.path().pointAtPercent(0.5).y() - (bound_rect_height // 2))

    def perform_evaluation_feedback(self):
        if self.timeline.state() == QtCore.QTimeLine.NotRunning:
            self.ellips_item.show()
            self.timeline.start()

    def end_evaluation_feedback(self):
        if self.timeline.state() == QtCore.QTimeLine.Running:
            self.ellips_item.hide()
            self.timeline.stop()

    def timeline_frame_changed(self, frame_num):
        if self.start_port.port_type == OUTPUT_NODE_TYPE:
            point = self.path().pointAtPercent(float(frame_num) / float(self.timeline.endFrame()))
        else:
            point = self.path().pointAtPercent(float(frame_num) / float(self.timeline.startFrame()))
        self.ellips_item.setPos(point)

    def get_input_node(self):
        if self.start_port.port_type == OUTPUT_NODE_TYPE:
            return self.end_port.get_node()
        else:
            return self.start_port.get_node()

    def get_output_node(self):
        if self.start_port.port_type == INPUT_NODE_TYPE:
            return self.end_port.get_node()
        else:
            return self.start_port.get_node()

    def get_output_type_port(self):
        if self.start_port.port_type == OUTPUT_NODE_TYPE:
            return self.start_port
        else:
            return self.end_port

    def get_input_type_port(self):
        if self.start_port.port_type == INPUT_NODE_TYPE:
            return self.start_port
        else:
            return self.end_port

    def delete_input_type_port(self, pos_destination=None):
        if self.start_port.port_type == OUTPUT_NODE_TYPE and self.end_port is not None:
            self.end_port.remove_pipes(self)
            self.end_port = None
        self.update_position(pos_destination)

    def intersect_with(self, p1, p2):
        cut_path = QtGui.QPainterPath(p1)
        cut_path.lineTo(p2)
        return cut_path.intersects(self.path())

    def update_position(self, pos_destination=None):
        self.pos_source = self.node.get_port_position(self.start_port.port_type, self.start_port.port_truth)
        if self.end_port is not None:
            self.pos_destination = self.end_port.parentItem().get_port_position(self.end_port.port_type,
                                                                                self.end_port.port_truth)
        elif pos_destination is not None:
            self.pos_destination = pos_destination
        else:
            self.pos_destination = self.pos_source
        self.update()

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
        sspos = self.start_port.port_type
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
        if self.end_port is None:
            painter.setPen(dragging_pen)
        else:
            painter.setPen(pen)

        # DRAW
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawPath(self.path())

        # ARROW
        image = QtGui.QPixmap("Resources/Pipe/arrow.png")
        image_rectf = QtCore.QRectF(image.rect().x(), image.rect().y(), image.rect().width(), image.rect().height())
        target_rectf = QtCore.QRectF(0, 0, 0, 0)
        if self.start_port.port_type == OUTPUT_NODE_TYPE:
            target_rectf = QtCore.QRectF(d.x() - 11, d.y() - 11, image.width(), image.height())
        elif self.start_port.port_type == INPUT_NODE_TYPE:
            target_rectf = QtCore.QRectF(s.x() - 11, s.y() - 11, image.width(), image.height())
        painter.drawPixmap(target_rectf, image, image_rectf)

        # EDIT
        bound_rect_width, bound_rect_height = self.edit.boundingRect().width(), self.edit.boundingRect().height()
        self.edit.setPos(self.path().pointAtPercent(0.5).x() - (bound_rect_width // 2),
                         self.path().pointAtPercent(0.5).y() - (bound_rect_height // 2))
