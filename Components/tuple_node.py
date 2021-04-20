from PyQt5 import QtWidgets, QtCore, QtGui
from Components import attribute
from Model import constants


__all__ = ["Node"]


class Node(QtWidgets.QGraphicsWidget):
    display_name_changed = QtCore.pyqtSignal(str)
    draw_label = None

    def __init__(self):
        super(Node, self).__init__()
        # SET BASIC FUNCTION.
        self.name = "Default NodeName"
        self.setFlags(QtWidgets.QGraphicsWidget.ItemIsMovable | QtWidgets.QGraphicsWidget.ItemIsSelectable |
                      QtWidgets.QGraphicsWidget.ItemIsFocusable | QtWidgets.QGraphicsWidget.ItemSendsGeometryChanges)
        self.setCacheMode(QtWidgets.QGraphicsItem.DeviceCoordinateCache)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setAcceptHoverEvents(True)
        self.setZValue(constants.Z_VAL_NODE)

        # COLOR AND SIZE OPTION
        self.style_properties = {
            'id': None,
            'name': self.name.strip(),
            'color': (229, 255, 255, 125),
            'border_color': (46, 57, 66, 255),
            'text_color': (255, 255, 255, 180),
            'width': constants.NODE_WIDTH,
            'height': constants.NODE_HEIGHT,
            'type_': 'Node',
            'selected': False,
            'disabled': False,
            'visible': False,
        }
        # GUI LAYOUT
        #   OVERALL LAYOUT
        self.node_layout = QtWidgets.QGraphicsLinearLayout(QtCore.Qt.Vertical)
        self.node_layout_margins = 5
        self.node_layout_spacing = 5
        self.node_layout.setContentsMargins(self.node_layout_margins, self.node_layout_margins,
                                            self.node_layout_margins, self.node_layout_margins)
        self.node_layout.setSpacing(self.node_layout_spacing)
        #   HEADER LAYOUT
        self.header_layout = QtWidgets.QGraphicsLinearLayout(QtCore.Qt.Horizontal)
        self.header_layout.setContentsMargins(0, 0, 0, 0)
        self.node_name_widget = attribute.NodeNameWidget(self)
        self.header_layout.setMaximumHeight(self.node_name_widget.sizeHint().height())
        self.header_layout.addItem(self.node_name_widget)
        self.node_layout.addItem(self.header_layout)
        self.setLayout(self.node_layout)
        # PORT
        self.input_port = attribute.Port(constants.INPUT_NODE_TYPE, self)
        self.output_port = attribute.Port(constants.OUTPUT_NODE_TYPE, self)
        # RESIZE
        self.resizing = False

        self.node_layout.addItem(attribute.LogicWidget(self))

    def paint(self, painter, option, widget=None) -> None:
        painter.save()
        # draw
        bg_border = 1.0
        rect = QtCore.QRectF(0.5 - (bg_border / 2),
                             0.5 - (bg_border / 2),
                             self.style_properties['width'] + bg_border,
                             self.style_properties['height'] + bg_border)
        radius = 2
        border_color = QtGui.QColor(*self.style_properties['border_color'])
        path = QtGui.QPainterPath()
        path.addRoundedRect(rect, radius, radius)

        # draw background
        rect = self.boundingRect()
        bg_color = QtGui.QColor(*self.style_properties['color'])
        painter.setBrush(bg_color if not self.isSelected() and constants.NODE_SEL_COLOR else QtGui.QColor(*constants.NODE_SEL_COLOR))
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRoundedRect(rect, radius, radius)

        label_rect = QtCore.QRectF(rect.left(), rect.top(), self.size().width(), 28)
        path = QtGui.QPainterPath()
        path.addRoundedRect(label_rect, radius, radius)
        painter.setBrush(QtGui.QColor(179, 217, 255, 200))
        painter.fillPath(path, painter.brush())

        border_width = 0.8
        if self.isSelected() and constants.NODE_SEL_BORDER_COLOR:
            border_width = 1.2
            border_color = QtGui.QColor(*constants.NODE_SEL_BORDER_COLOR)
        border_rect = QtCore.QRectF(rect.left() - (border_width / 2),
                             rect.top() - (border_width / 2),
                             rect.width() + border_width,
                             rect.height() + border_width)
        pen = QtGui.QPen(border_color, border_width)
        path = QtGui.QPainterPath()
        path.addRoundedRect(border_rect, radius, radius)
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.setPen(pen)
        painter.drawPath(path)

        # DRAW PORT
        self.input_port.setPos(-10, self.size().height() / 2)
        self.output_port.setPos(self.size().width() - 10, self.size().height() / 2)

        painter.restore()

    def update_node_shape(self):
        self.prepareGeometryChange()
        self.node_layout.invalidate()
        self.updateGeometry()
        self.update()
        self.node_name_widget.updateGeometry()
        self.node_name_widget.update()

    def get_port_position(self, port_type):
        x = -10 if port_type == constants.INPUT_NODE_TYPE else self.size().width() - 10
        y = self.size().height() / 2
        return x, y

    def mousePressEvent(self, event) -> None:
        if int(event.modifiers()) & QtCore.Qt.ShiftModifier:
            self.resizing = True
            self.setCursor(QtCore.Qt.SizeAllCursor)
        else:
            super(Node, self).mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:
        if self.resizing:
            past_pos = self.scenePos()
            past_width = self.size().width()
            past_height = self.size().height()
            current_pos = self.mapToScene(event.pos())
            current_width = current_pos.x() - past_pos.x() if current_pos.x() >= past_pos.x() else past_width
            current_height = current_pos.y() - past_pos.y() if current_pos.y() >= past_pos.y() else past_height

            self.resize(current_width, current_height)
            if constants.DEBUG_TUPLE_NODE_SCALE:
                print(current_width, current_height)
        else:
            super(Node, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        if self.resizing:
            self.resizing = False
            self.setCursor(QtCore.Qt.ArrowCursor)
        else:
            super(Node, self).mouseReleaseEvent(event)
