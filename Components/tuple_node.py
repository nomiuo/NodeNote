from PyQt5.QtWidgets import QGraphicsLinearLayout
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QColor, QPainterPath, QPen
from Components.port import Port
from Components.property import *
from Model.constants import *


class Node(QGraphicsWidget):
    display_name_changed = pyqtSignal(str)
    draw_label = None

    def __init__(self):
        super(Node, self).__init__()
        # SET BASIC FUNCTION.
        self.name = "Default NodeName"
        self.setFlags(QGraphicsWidget.ItemIsMovable | QGraphicsWidget.ItemIsSelectable |
                      QGraphicsWidget.ItemIsFocusable | QGraphicsWidget.ItemSendsGeometryChanges)
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setAcceptHoverEvents(True)
        self.setZValue(Z_VAL_NODE)

        # COLOR AND SIZE OPTION
        self.style_properties = {
            'id': None,
            'name': self.name.strip(),
            'color': (229, 255, 255, 125),
            'border_color': (46, 57, 66, 255),
            'text_color': (255, 255, 255, 180),
            'width': NODE_WIDTH,
            'height': NODE_HEIGHT,
            'type_': 'Node',
            'selected': False,
            'disabled': False,
            'visible': False,
        }
        # GUI LAYOUT
        #   OVERALL LAYOUT
        self.node_layout = QGraphicsLinearLayout(Qt.Vertical)
        self.node_layout_margins = 5
        self.node_layout_spacing = 5
        self.node_layout.setContentsMargins(self.node_layout_margins, self.node_layout_margins,
                                            self.node_layout_margins, self.node_layout_margins)
        self.node_layout.setSpacing(self.node_layout_spacing)
        #   HEADER LAYOUT
        self.header_layout = QGraphicsLinearLayout(Qt.Horizontal)
        self.header_layout.setContentsMargins(0, 0, 0, 0)
        self.node_name = NodeNameWidget(self)
        self.header_layout.setMaximumHeight(self.node_name.sizeHint().height())
        self.header_layout.addItem(self.node_name)
        self.node_layout.addItem(self.header_layout)
        self.setLayout(self.node_layout)
        self.node_layout.addItem(TestWidget("hello", self))
        # PORT
        self.input_port = Port(INPUT_NODE_TYPE, self)
        self.output_port = Port(OUTPUT_NODE_TYPE, self)
        # RESIZE
        self.resizing = False

    def paint(self, painter, option, widget=None) -> None:
        painter.save()
        # draw
        bg_border = 1.0
        rect = QRectF(0.5 - (bg_border / 2),
                      0.5 - (bg_border / 2),
                      self.style_properties['width'] + bg_border,
                      self.style_properties['height'] + bg_border)
        radius = 2
        border_color = QColor(*self.style_properties['border_color'])
        path = QPainterPath()
        path.addRoundedRect(rect, radius, radius)

        # draw background
        rect = self.boundingRect()
        bg_color = QColor(*self.style_properties['color'])
        painter.setBrush(bg_color if not self.isSelected() and NODE_SEL_COLOR else QColor(*NODE_SEL_COLOR))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, radius, radius)

        label_rect = QRectF(rect.left(), rect.top(), self.size().width(), 28)
        path = QPainterPath()
        path.addRoundedRect(label_rect, radius, radius)
        painter.setBrush(QColor(179, 217, 255, 200))
        painter.fillPath(path, painter.brush())

        border_width = 0.8
        if self.isSelected() and NODE_SEL_BORDER_COLOR:
            border_width = 1.2
            border_color = QColor(*NODE_SEL_BORDER_COLOR)
        border_rect = QRectF(rect.left() - (border_width / 2),
                             rect.top() - (border_width / 2),
                             rect.width() + border_width,
                             rect.height() + border_width)
        pen = QPen(border_color, border_width)
        path = QPainterPath()
        path.addRoundedRect(border_rect, radius, radius)
        painter.setBrush(Qt.NoBrush)
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
        self.node_name.updateGeometry()
        self.node_name.update()

    def mousePressEvent(self, event) -> None:
        if int(event.modifiers()) & Qt.ShiftModifier:
            self.resizing = True
            self.setCursor(Qt.SizeAllCursor)
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
            if DEBUG_TUPLE_NODE_SCALE:
                print(current_width, current_height)
        else:
            super(Node, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        if self.resizing:
            self.resizing = False
            self.setCursor(Qt.ArrowCursor)
        else:
            super(Node, self).mouseReleaseEvent(event)
