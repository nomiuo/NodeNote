from collections import OrderedDict
from PyQt5 import QtGui, QtCore, QtWidgets
from Model import constants, serializable
from Components import attribute

__all__ = ["Pipe"]


class Pipe(QtWidgets.QGraphicsPathItem, serializable.Serializable):
    def __init__(self, start_port=None, end_port=None, node=None):
        super(Pipe, self).__init__()
        self.node = node
        self.start_port = start_port
        self.end_port = end_port

        # BASIC SETTINGS
        self.setFlags(QtWidgets.QGraphicsItem.ItemIsSelectable)
        self.setZValue(constants.Z_VAL_PIPE)

        # DRAW PARAMETERS
        self.color = QtGui.QColor(0, 255, 204, 128)
        self.selected_color = QtGui.QColor(0, 153, 121, 255)

        # POS
        self.pos_source = self.start_port.parentItem().get_port_position(self.start_port.port_type,
                                                                         self.start_port.port_truth)
        self.pos_destination = self.pos_source
        self.control_start_point = QtCore.QPointF()
        self.control_end_point = QtCore.QPointF()
        self.status = constants.PIPE_STATUS_NEW

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
        if start_port.port_type == constants.OUTPUT_NODE_TYPE:
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

        # CONTROL
        self.control_start_point_offect = QtCore.QPointF()
        self.control_end_point_offect = QtCore.QPointF()
        self.defalut_start_offect = None
        self.default_end_offect = None
        self.move_status = constants.PIPE_FIRST
        self.choose_first = True
        self.distance_end = None
        self.distance_start = None
        self.last_default_start = QtCore.QPointF()
        self.last_default_end = QtCore.QPointF()
        self.now_default_start = None
        self.now_default_end = None
        self.control = False

    def perform_evaluation_feedback(self):
        if self.timeline.state() == QtCore.QTimeLine.NotRunning:
            self.ellips_item.show()
            self.timeline.start()

    def end_evaluation_feedback(self):
        if self.timeline.state() == QtCore.QTimeLine.Running:
            self.ellips_item.hide()
            self.timeline.stop()

    def timeline_frame_changed(self, frame_num):
        if self.start_port.port_type == constants.OUTPUT_NODE_TYPE:
            point = self.path().pointAtPercent(float(frame_num) / float(self.timeline.endFrame()))
        else:
            point = self.path().pointAtPercent(float(frame_num) / float(self.timeline.startFrame()))
        self.ellips_item.setPos(point)

    def get_input_node(self):
        if self.start_port.port_type == constants.OUTPUT_NODE_TYPE:
            return self.end_port.get_node()
        else:
            return self.start_port.get_node()

    def get_output_node(self):
        if self.start_port.port_type == constants.INPUT_NODE_TYPE:
            return self.end_port.get_node()
        else:
            return self.start_port.get_node()

    def get_output_type_port(self):
        if self.start_port.port_type == constants.OUTPUT_NODE_TYPE:
            return self.start_port
        else:
            return self.end_port

    def get_input_type_port(self):
        if self.start_port.port_type == constants.INPUT_NODE_TYPE:
            return self.start_port
        else:
            return self.end_port

    def delete_input_type_port(self, pos_destination=None):
        if self.start_port.port_type == constants.OUTPUT_NODE_TYPE and self.end_port is not None:
            self.end_port.remove_pipes(self)
            self.end_port = None
        self.update_position(pos_destination)

    def intersect_with(self, p1, p2):
        cut_path = QtGui.QPainterPath(p1)
        cut_path.lineTo(p2)
        if constants.DEBUG_CUT_LINE:
            print(self, ": ", cut_path.intersects(self.path()))
        return cut_path.intersects(self.path())

    def update_position(self, pos_destination=None):
        self.pos_source = self.start_port.parentItem().get_port_position(self.start_port.port_type,
                                                                         self.start_port.port_truth)
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
        if ((s.x() > d.x()) and sspos == constants.OUTPUT_NODE_TYPE) or \
                ((s.x() < d.x()) and sspos == constants.INPUT_NODE_TYPE):
            s_x *= -1  # > 0, s_y = 0  | < 0
            d_x *= -1  # < 0, d_y = 0  | > 0

        path = QtGui.QPainterPath(self.pos_source)
        if self.move_status == constants.PIPE_FIRST:
            self.defalut_start_offect = QtCore.QPointF(s.x() + s_x, s.y() + s_y)
            self.default_end_offect = QtCore.QPointF(d.x() + d_x, d.y() + d_y)
            self.last_default_start = QtCore.QPointF(s.x() + s_x, s.y() + s_y)
            self.last_default_end = QtCore.QPointF(d.x() + d_x, d.y() + d_y)
            self.control_start_point = self.defalut_start_offect
            self.control_end_point = self.default_end_offect
        elif self.move_status == constants.PIPE_MOVEING:
            self.control_start_point = self.defalut_start_offect + self.control_start_point_offect
            self.control_end_point = self.default_end_offect + self.control_end_point_offect
        elif self.move_status == constants.PIPE_COMMON:
            self.defalut_start_offect = self.control_start_point
            self.default_end_offect = self.control_end_point
            self.move_status = constants.PIPE_UPDATE
        elif self.move_status == constants.PIPE_UPDATE:
            self.control_start_point += QtCore.QPointF(s.x() + s_x, s.y() + s_y) - self.last_default_start
            self.control_end_point += QtCore.QPointF(d.x() + d_x, d.y() + d_y) - self.last_default_end
            self.last_default_start = QtCore.QPointF(s.x() + s_x, s.y() + s_y)
            self.last_default_end = QtCore.QPointF(d.x() + d_x, d.y() + d_y)
        path.cubicTo(
            self.control_start_point,
            self.control_end_point,
            self.pos_destination
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
        if self.start_port.port_type == constants.OUTPUT_NODE_TYPE:
            target_rectf = QtCore.QRectF(d.x() - 11, d.y() - 11, image.width(), image.height())
        elif self.start_port.port_type == constants.INPUT_NODE_TYPE:
            target_rectf = QtCore.QRectF(s.x() - 11, s.y() - 11, image.width(), image.height())
        painter.drawPixmap(target_rectf, image, image_rectf)

        # EDIT
        bound_rect_width, bound_rect_height = self.edit.boundingRect().width(), self.edit.boundingRect().height()
        self.edit.setPos(self.path().pointAtPercent(0.5).x() - (bound_rect_width // 2),
                         self.path().pointAtPercent(0.5).y() - (bound_rect_height // 2))

    def mouseMoveEvent(self, event: 'QtWidgets.QGraphicsSceneMouseEvent') -> None:
        if self.isSelected():
            self.move_status = constants.PIPE_MOVEING
            current_pos = event.scenePos()
            if self.choose_first:
                self.distance_start = (current_pos.x() - self.defalut_start_offect.x()) ** 2 + \
                                      (current_pos.y() - self.defalut_start_offect.y()) ** 2
                self.distance_end = (current_pos.x() - self.default_end_offect.x()) ** 2 + \
                                    (current_pos.y() - self.default_end_offect.y()) ** 2
                self.choose_first = False
            if self.distance_start > self.distance_end:
                self.control_start_point_offect = QtCore.QPointF()
                self.control_end_point_offect = event.scenePos()
            else:
                self.control_start_point_offect = event.scenePos()
                self.control_end_point_offect = QtCore.QPointF()
            self.control = True
            self.update()

    def mouseReleaseEvent(self, event: 'QtWidgets.QGraphicsSceneMouseEvent') -> None:
        super(Pipe, self).mouseReleaseEvent(event)
        self.move_status = constants.PIPE_COMMON
        self.choose_first = True
        if self.isSelected() and self.control:
            self.scene().view.history.store_history("Change Pipe Control Point")
            self.control = False

    def serialize(self):
        # if not self.last_default_start or not self.last_default_end:
        #     s = self.pos_source
        #     d = self.pos_destination
        #     dist = (d.x() - s.x()) * 0.5
        #     sspos = self.start_port.port_type
        #     s_x = +dist
        #     s_y = 0
        #     d_x = -dist
        #     d_y = 0
        #     if ((s.x() > d.x()) and sspos == constants.OUTPUT_NODE_TYPE) or \
        #             ((s.x() < d.x()) and sspos == constants.INPUT_NODE_TYPE):
        #         s_x *= -1  # > 0, s_y = 0  | < 0
        #         d_x *= -1  # < 0, d_y = 0  | > 0
        #     self.last_default_start = QtCore.QPointF(s.x() + s_x, s.y() + s_y)
        #     self.last_default_end = QtCore.QPointF(d.x() + d_x, d.y() + d_y)

        return OrderedDict([
            ('id', self.id),
            ('start port', self.start_port.id),
            ('end port', self.end_port.id),
            ("text", self.edit.toPlainText()),
            ('start control point x', self.control_start_point.x()),
            ('start control point y', self.control_start_point.y()),
            ('end control point x', self.control_end_point.x()),
            ('end control point y', self.control_end_point.y()),
            ('last default start point x', self.last_default_start.x()),
            ('last default start point y', self.last_default_start.y()),
            ('last default end point x', self.last_default_end.x()),
            ('last default end point y', self.last_default_end.y())
        ])

    def deserialize(self, data, hashmap: dict, view=None, flag=True):
        # added into current scene and view
        view.current_scene.addItem(self)
        view.pipes.append(self)
        # id and hashmap
        self.id = data['id']
        hashmap[data['id']] = self
        # text
        self.edit.setPlainText(data['text'])
        # control point
        self.control_start_point = QtCore.QPointF(data['start control point x'], data['start control point y'])
        self.control_end_point = QtCore.QPointF(data['end control point x'], data['end control point y'])
        self.last_default_start = QtCore.QPointF(data['last default start point x'], data['last default start point y'])
        self.last_default_end = QtCore.QPointF(data['last default end point x'], data['last default end point y'])
        self.move_status = constants.PIPE_COMMON
        self.update()
        return True
