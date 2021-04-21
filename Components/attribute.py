from PyQt5 import QtCore, QtWidgets, QtGui
from Model import constants, stylesheet
from Components import port

__all__ = ["SubConstituteWidget", "InputTextField",
           "LogicWidget", "TruthWidget", "AttributeWidget"]


class InputTextField(QtWidgets.QGraphicsTextItem):
    edit_finished = QtCore.pyqtSignal(bool)
    start_editing = QtCore.pyqtSignal()

    def __init__(self, text, node, parent=None, single_line=False):
        super(InputTextField, self).__init__(text, parent)
        self.node = node
        self.single_line = single_line
        self.text_before_editing = ""
        self.origMoveEvent = self.mouseMoveEvent
        self.mouseMoveEvent = self.node.mouseMoveEvent
        # SET BASIC FUNCTION
        self.basic_function()

    def basic_function(self):
        self.setFlags(QtWidgets.QGraphicsWidget.ItemSendsGeometryChanges | QtWidgets.QGraphicsWidget.ItemIsSelectable)
        self.setObjectName("Nothing")

    def keyPressEvent(self, event) -> None:
        # insert key text into text field.
        current_key = event.key()

        # restore text before editing and return.
        if current_key == QtCore.Qt.Key_Escape:
            self.setPlainText(self.text_before_editing)
            self.clearFocus()
            super(InputTextField, self).keyPressEvent(event)
            return

        # once press enter or return, it will not wrap around
        if self.single_line:
            if current_key in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
                if self.toPlainText() == "":
                    self.setPlainText(self.text_before_editing)
                    event.ignore()
                    self.edit_finished.emit(False)
                    self.clearFocus()
                else:
                    event.ignore()
                    self.clearFocus()
            else:
                super(InputTextField, self).keyPressEvent(event)
        else:
            super(InputTextField, self).keyPressEvent(event)

    def mousePressEvent(self, event) -> None:
        # change focus into node
        if self.objectName() == "MouseLocked":
            super(InputTextField, self).mousePressEvent(event)
        else:
            self.node.mousePressEvent(event)
            self.clearFocus()

    def mouseReleaseEvent(self, event) -> None:
        # change focus into node
        if self.objectName() == "MouseLocked":
            super(InputTextField, self).mouseReleaseEvent(event)
        else:
            self.node.mouseReleaseEvent(event)
            self.clearFocus()

    def mouseDoubleClickEvent(self, event) -> None:
        # get focus
        super(InputTextField, self).mouseDoubleClickEvent(event)
        self.setFlag(QtWidgets.QGraphicsWidget.ItemIsFocusable, True)
        self.start_editing.emit()
        self.setFocus()

    def focusInEvent(self, event) -> None:
        self.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.setObjectName("MouseLocked")
        self.text_before_editing = self.toPlainText()
        self.mouseMoveEvent = self.origMoveEvent
        super(InputTextField, self).focusInEvent(event)

    def focusOutEvent(self, event) -> None:
        # clear selection
        cursor = self.textCursor()
        cursor.clearSelection()
        self.setTextCursor(cursor)
        super(InputTextField, self).focusOutEvent(event)
        self.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.setObjectName("Nothing")
        if self.toPlainText() == "":
            self.setPlainText(self.text_before_editing)
            self.edit_finished.emit(False)
        else:
            self.edit_finished.emit(True)
        self.mouseMoveEvent = self.node.mouseMoveEvent


class SubConstituteWidget(QtWidgets.QGraphicsWidget):
    def __init__(self, parent=None):
        super(SubConstituteWidget, self).__init__(parent)
        # SET BASIC FUNCTION
        self.hovered = False
        self.setAcceptHoverEvents(True)
        self.setFlag(QtWidgets.QGraphicsWidget.ItemSendsGeometryChanges)
        self.setCacheMode(QtWidgets.QGraphicsItem.DeviceCoordinateCache)

        # LABEL ITEM
        self.label_item = InputTextField(self.parentItem().name, parent, self,
                                         single_line=False)
        self.label_font = QtGui.QFont("Consolas")
        self.label_item.setAcceptHoverEvents(True)
        self.label_item.document().contentsChanged.connect(self.parentItem().update_node_shape)
        self.label_item.hoverMoveEvent = self.hoverMoveEvent
        self.label_font.setPointSize(6)

        self.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        self.layout = QtWidgets.QGraphicsLinearLayout(QtCore.Qt.Horizontal)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.label_widget = QtWidgets.QGraphicsWidget()
        self.label_widget.setGraphicsItem(self.label_item)
        self.layout.addItem(self.label_widget)
        self.setLayout(self.layout)

    def hoverEnterEvent(self, event) -> None:
        super(SubConstituteWidget, self).hoverEnterEvent(event)
        self.hovered = True
        self.update()

    def hoverMoveEvent(self, event) -> None:
        self.parentItem().hoverMoveEvent(event)

    def hoverLeaveEvent(self, event) -> None:
        super(SubConstituteWidget, self).hoverLeaveEvent(event)
        self.hovered = False
        self.update()

    def sizeHint(self, which=None, constraint=None) -> QtCore.QSizeF:
        width = self.label_item.boundingRect().width()
        height = self.label_item.boundingRect().height() + 5
        return QtCore.QSizeF(width, height)


class GroupWidget(QtWidgets.QGroupBox):
    def __init__(self, label, parent=None):
        super(GroupWidget, self).__init__(parent)
        layout = QtWidgets.QHBoxLayout(self)
        layout.setSpacing(4)
        self.setTitle(label)

    def setTitle(self, text):
        margin = (0, 0, 0, 0)
        padding_top = '14px'
        if text == '':
            margin = (0, 2, 0, 0)
            padding_top = '2px'
        style = stylesheet.STYLE_QGROUPBOX.replace('$PADDING_TOP', padding_top)
        self.layout().setContentsMargins(*margin)
        self.setStyleSheet(style)
        super(GroupWidget, self).setTitle(text)

    def add_node_widget(self, widget):
        self.layout().addWidget(widget)

    def get_node_widget(self):
        return self.layout().itemAt(0).widget()


class AbstractWidget(QtWidgets.QGraphicsWidget):
    def __init__(self, parent):
        super(AbstractWidget, self).__init__(parent)
        self.resizing = False

    def mousePressEvent(self, event) -> None:
        if int(event.modifiers()) & QtCore.Qt.ShiftModifier:
            self.resizing = True
            if constants.DEBUG_TUPLE_NODE_SCALE:
                print("Node is scaling!")
            self.setCursor(QtCore.Qt.SizeAllCursor)
        else:
            super(AbstractWidget, self).mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:
        if self.resizing:
            past_pos = self.scenePos()
            past_width = self.size().width()
            past_height = self.size().height()
            current_pos = self.mapToScene(event.pos())
            current_width = current_pos.x() - past_pos.x() if current_pos.x() >= past_pos.x() else past_width
            current_height = current_pos.y() - past_pos.y() if current_pos.y() >= past_pos.y() else past_height
            if current_width >= self.childItems()[0].widget().minimumSize().width() and \
                    current_height >= self.childItems()[0].widget().minimumSize().height():
                self.resize(current_width, current_height)
            if constants.DEBUG_TUPLE_NODE_SCALE:
                print("DEBUG TUPLE NODE SCALE CURRENT SIZE:", current_width, current_height)
        else:
            super(AbstractWidget, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        if self.resizing:
            self.resizing = False
            self.setCursor(QtCore.Qt.ArrowCursor)
        else:
            super(AbstractWidget, self).mouseReleaseEvent(event)


class LogicWidget(AbstractWidget):
    def __init__(self, scene, parent=None):
        super(LogicWidget, self).__init__(parent)
        self.resizing = False
        self.scene = scene
        self.setFlags(QtWidgets.QGraphicsItem.ItemIsMovable | QtWidgets.QGraphicsItem.ItemIsSelectable)
        self.input_port = port.Port(constants.INPUT_NODE_TYPE, self)
        self.output_port = port.Port(constants.OUTPUT_NODE_TYPE, self)
        self.layout = QtWidgets.QGraphicsLinearLayout()
        self.design_ui()

    def design_ui(self):
        # select logic
        logic_combobox_input = QtWidgets.QComboBox()
        logic_combobox_input.setStyleSheet(stylesheet.STYLE_QCOMBOBOX)
        logic_combobox_input.setMaximumHeight(20)
        logic_list_input = QtWidgets.QListView(logic_combobox_input)
        logic_list_input.setStyleSheet(stylesheet.STYLE_QLISTVIEW)
        logic_combobox_input.setView(logic_list_input)
        logic_combobox_input.addItems(("And", "Or", "Not"))
        logic_combobox_input.clearFocus()

        logic_combobox_output = QtWidgets.QComboBox()
        logic_combobox_output.setStyleSheet(stylesheet.STYLE_QCOMBOBOX)
        logic_combobox_input.setMaximumHeight(20)
        logic_list_output = QtWidgets.QListView(logic_combobox_output)
        logic_list_output.setStyleSheet(stylesheet.STYLE_QLISTVIEW)
        logic_combobox_output.setView(logic_list_output)
        logic_combobox_output.addItems(("And", "Or", "Not"))
        logic_combobox_output.clearFocus()

        group = GroupWidget("Logical Controller")
        group.add_node_widget(logic_combobox_input)
        group.add_node_widget(logic_combobox_output)
        proxywidget = QtWidgets.QGraphicsProxyWidget()
        proxywidget.setWidget(group)
        self.layout.addItem(proxywidget)
        self.setLayout(self.layout)

    def paint(self, painter, option, widget=None) -> None:
        super(LogicWidget, self).paint(painter, option, widget)
        self.input_port.setPos(-12, self.size().height() / 2 - 3)
        self.output_port.setPos(self.size().width() - 12, self.size().height() / 2 - 3)

        painter.setPen(QtGui.QPen(QtGui.QColor(15, 242, 254, 255), 3))
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawRoundedRect(0, 0, self.size().width(), self.size().height(), 2, 2)


class TruthWidget(QtWidgets.QGraphicsWidget):
    def __init__(self, parent=None):
        super(TruthWidget, self).__init__(parent)
        # new checkbox
        self.truth_checkbox = QtWidgets.QCheckBox("Truth")
        self.truth_checkbox.setChecked(True)
        self.truth_checkbox.setStyleSheet(stylesheet.STYLE_QCHECKBOX)

        # set font
        font = self.truth_checkbox.font()
        font.setPointSize(8)
        self.truth_checkbox.setFont(font)

        # add into group
        proxywidget = QtWidgets.QGraphicsProxyWidget()
        proxywidget.setWidget(self.truth_checkbox)
        self.layout = QtWidgets.QGraphicsLinearLayout(QtCore.Qt.Horizontal)
        self.layout.addItem(proxywidget)
        self.setLayout(self.layout)


# todo: 1. resize not working, maybe use stretch
# todo: 2. add two hide-able widgets Done
# todo: 3. resize parent hide-able size when chidren's hidden widget showed
# todo: 4. input text over rows and size go wrong when delete row text
class AttributeWidget(QtWidgets.QGraphicsWidget):
    display_name_changed = QtCore.pyqtSignal(str)
    draw_label = None

    def __init__(self):
        super(AttributeWidget, self).__init__()
        # SET BASIC FUNCTION.
        self.name = "Default Attribute Name"
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
        self.sub_constitute_widget = SubConstituteWidget(self)
        self.hidden_able_pic = QtGui.QPixmap("Resources/down_arrow.png")
        self.hidden_able_widget = QtWidgets.QGraphicsWidget()
        self.hidden_able_widget.setMaximumSize(20.0, 20.0)
        self.hidden_able_widget.setMinimumSize(20.0, 20.0)
        palette = self.hidden_able_widget.palette()
        palette.setBrush(QtGui.QPalette.Window, QtGui.QBrush(self.hidden_able_pic))
        self.hidden_able_widget.setAutoFillBackground(True)
        self.hidden_able_widget.setPalette(palette)
        self.header_layout.addItem(self.sub_constitute_widget)
        self.header_layout.insertStretch(1, 1)
        self.header_layout.addItem(self.hidden_able_widget)
        self.header_layout.setAlignment(self.hidden_able_widget, QtCore.Qt.AlignRight)
        #   STATUS LAYOUT
        self.status_widget = QtWidgets.QGraphicsWidget()
        self.status_widget.setAutoFillBackground(True)
        self.status_widget_visiable = False
        self.status_widget.setVisible(self.status_widget_visiable)
        palette = self.status_widget.palette()
        palette.setBrush(QtGui.QPalette.Window, QtGui.QBrush(QtGui.QColor(255, 229, 229, 128)))
        self.status_widget.setPalette(palette)
        self.status_layout = QtWidgets.QGraphicsLinearLayout(QtCore.Qt.Horizontal)
        self.status_layout.setContentsMargins(0, 0, 0, 0)
        self.status_truth = TruthWidget()
        self.status_time = SubConstituteWidget(self)
        self.status_layout.addItem(self.status_truth)
        self.status_layout.addItem(self.status_time)
        self.status_layout.setAlignment(self.status_time, QtCore.Qt.AlignBottom)
        self.status_layout.setAlignment(self.status_truth, QtCore.Qt.AlignBottom)
        self.status_widget.setLayout(self.status_layout)
        #   ATTRIBUTE LAYOUT
        self.attribute_layout = QtWidgets.QGraphicsLinearLayout(QtCore.Qt.Horizontal)
        self.attribute_layout.setContentsMargins(0, 0, 0, 0)
        # ALL LAYOUT
        self.node_layout.addItem(self.header_layout)
        self.node_layout.addItem(self.attribute_layout)
        self.node_layout.addItem(self.status_widget)
        self.setLayout(self.node_layout)

        # PORT
        self.input_port = port.Port(constants.INPUT_NODE_TYPE, self)
        self.output_port = port.Port(constants.OUTPUT_NODE_TYPE, self)

        # RESIZE
        self.resizing = False
        # WIDGET LIST

        self.widget_list = list()

    def paint(self, painter, option, widget=None) -> None:
        painter.save()
        # draw
        bg_border = 1.0
        rect = QtCore.QRectF(0.5 - (bg_border / 2),
                             0.5 - (bg_border / 2),
                             self.boundingRect().width() + bg_border,
                             self.boundingRect().height() + bg_border)
        radius = 2
        border_color = QtGui.QColor(*self.style_properties['border_color'])
        path = QtGui.QPainterPath()
        path.addRoundedRect(rect, radius, radius)

        # draw background
        rect = self.boundingRect()
        bg_color = QtGui.QColor(*self.style_properties['color'])
        painter.setBrush(
            bg_color if not self.isSelected() and constants.NODE_SEL_COLOR else QtGui.QColor(*constants.NODE_SEL_COLOR))
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRoundedRect(rect, radius, radius)

        label_rect = QtCore.QRectF(rect.left(), rect.top(), self.size().width(),
                                   self.sub_constitute_widget.sizeHint().height())
        path = QtGui.QPainterPath()
        path.addRoundedRect(label_rect, radius, radius)
        painter.setBrush(QtGui.QColor(179, 217, 255, 200))
        painter.fillPath(path, painter.brush())

        # draw border
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
        self.input_port.setPos(-12, self.sub_constitute_widget.sizeHint().height() / 2)
        self.output_port.setPos(self.size().width() - 10, self.sub_constitute_widget.sizeHint().height() / 2)

        # RESIZE
        current_size = QtCore.QSizeF(self.sub_constitute_widget.sizeHint().width(),
                                     self.sub_constitute_widget.size().height() if self.status_widget_visiable else \
                                         self.size().height())
        self.resize(current_size)

        painter.restore()

    def update_node_shape(self):
        self.prepareGeometryChange()
        self.node_layout.invalidate()
        self.updateGeometry()
        self.update()
        self.sub_constitute_widget.updateGeometry()
        self.sub_constitute_widget.update()
        self.status_time.updateGeometry()
        self.status_time.update()

    def mouse_update_node_size(self, event):
        past_pos = self.scenePos()
        past_width = self.size().width()
        past_height = self.size().height()
        current_pos = self.mapToScene(event.pos())
        current_width = current_pos.x() - past_pos.x() if current_pos.x() >= past_pos.x() else past_width
        current_height = current_pos.y() - past_pos.y() if current_pos.y() >= past_pos.y() else past_height

        self.resize(current_width, current_height)
        if constants.DEBUG_TUPLE_NODE_SCALE:
            print(current_width, current_height)

    def show_hidden_attributes(self, event):
        if constants.DEBUG_SHOW_HIDDEN_ATTRIBUTES:
            print("DEBUG: SHOW HIDDEN ATTRIBUTES")
        self.status_widget_visiable = not self.status_widget_visiable
        self.status_widget.setVisible(self.status_widget_visiable)
        self.update_node_shape()
        self.mouse_update_node_size(event)

    def get_port_position(self, port_type):
        x = -10 if port_type == constants.INPUT_NODE_TYPE else self.size().width() - 10
        y = self.size().height() / 2
        return x, y

    def add_subwidget(self):
        subwidget = AttributeWidget()
        self.attribute_layout.addItem(subwidget)

    def mousePressEvent(self, event) -> None:
        if int(event.modifiers()) & QtCore.Qt.ShiftModifier:
            self.resizing = True
            self.setCursor(QtCore.Qt.SizeAllCursor)

        current_widget = self.scene().itemAt(event.scenePos(), QtGui.QTransform())
        if constants.DEBUG_SHOW_HIDDEN_ATTRIBUTES:
            print("DEBUG: SHOW CURRENT WIDGET", current_widget, "AT", event.scenePos())
        if current_widget is self.hidden_able_widget:
            self.show_hidden_attributes(event)
            super(AttributeWidget, self).mousePressEvent(event)
        else:
            super(AttributeWidget, self).mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:
        if self.resizing:
            self.mouse_update_node_size(event)
        else:
            super(AttributeWidget, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        if self.resizing:
            self.resizing = False
            self.setCursor(QtCore.Qt.ArrowCursor)
        else:
            super(AttributeWidget, self).mouseReleaseEvent(event)

    def contextMenuEvent(self, event: 'QtWidgets.QGraphicsSceneContextMenuEvent') -> None:
        menu = QtWidgets.QMenu()
        menu.setStyleSheet(stylesheet.STYLE_QMENU)
        add_subwidget = menu.addAction("Add Subwidget")
        add_subwidget.setIcon(QtGui.QIcon("Resources/AttributeWidgetContextMenu/ADD SUBWIDGET.PNG"))
        result = menu.exec(event.screenPos())
        if result == add_subwidget:
            self.add_subwidget()
        event.setAccepted(True)
