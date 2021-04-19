from PyQt5.QtWidgets import QGraphicsProxyWidget, QComboBox, QListView, QGroupBox, QVBoxLayout, QStyle, QCheckBox, \
    QTextEdit, QGraphicsTextItem, QGraphicsWidget, QSizePolicy, QMenu, QGraphicsLinearLayout
from PyQt5.QtCore import pyqtSignal, Qt, QRegExp, QSizeF, QRectF
from PyQt5 import QtCore
from PyQt5.QtGui import QFontMetrics, QTextDocument, QRegExpValidator, QValidator, QFont, QColor, \
    QPainterPath, QPen, QIcon
from Model.constants import *
from Model.stylesheet import *


class GroupWidget(QGroupBox):
    def __init__(self, label, parent=None):
        super(GroupWidget, self).__init__(parent)
        layout = QVBoxLayout(self)
        layout.setSpacing(1)
        self.setTitle(label)

    def setTitle(self, text):
        margin = (0, 0, 0, 0)
        padding_top = '14px'
        if text == '':
            margin = (0, 2, 0, 0)
            padding_top = '2px'
        style = STYLE_QGROUPBOX.replace('$PADDING_TOP', padding_top)
        self.layout().setContentsMargins(*margin)
        self.setStyleSheet(style)
        super(GroupWidget, self).setTitle(text)

    def add_node_widget(self, widget):
        self.layout().addWidget(widget)

    def get_node_widget(self):
        return self.layout().itemAt(0).widget()


class BaseWidget(QGraphicsProxyWidget):
    value_changed = pyqtSignal(str, object)

    def __init__(self, parent=None, name=None, label='', ):
        super(BaseWidget, self).__init__(parent)
        self.name = name
        self.label = label
        self.node = None
        self.setZValue(Z_VAL_NODE_WIDGET + 1)

    def setToolTip(self, tooltip):
        tooltip = tooltip.replace('\n', '<br/>')
        tooltip = '<b>{}</b><br/>{}'.format(self.name, tooltip)
        super(BaseWidget, self).setToolTip(tooltip)

    def on_value_changed(self):
        # pycharm bug with emit
        self.value_changed.emit(self.name, self.get_value())

    def get_value(self):
        raise NotImplementedError

    def set_value(self, text):
        raise NotImplementedError

    def get_custom_widget(self):
        widget = self.widget()
        return widget.get_node_widget()

    def set_custom_widget(self, widget):
        if self.widget():
            raise Exception('Custom node widget already set.')
        group = GroupWidget(self.label)
        group.add_node_widget(widget)
        self.setWidget(group)

    def set_name(self, name):
        if not name:
            return
        if self.node:
            raise Exception(
                'Can\'t set property name widget already added to a Node'
            )
        self.name = name

    def set_label(self, label=''):
        if self.widget():
            self.widget().setTitle(label)
        self.label = label

    def get_icon(self, name):
        return self.style().standardIcon(QStyle.StandardPixmap(name))


class TestWidget(BaseWidget):
    def __init__(self, label='', name=None, items=None, parent=None):
        super(TestWidget, self).__init__(parent)
        self.label = label
        self.name = name
        self.items = items
        self.design_ui()

    def design_ui(self):
        # select logic
        logic_combobox = QComboBox()
        logic_combobox.setStyleSheet(STYLE_QCOMBOBOX)
        logic_combobox.setMinimumHeight(24)
        # items
        logic_list = QListView(logic_combobox)
        logic_list.setStyleSheet(STYLE_QLISTVIEW)
        logic_combobox.setView(logic_list)
        logic_combobox.addItems(self.items or list())
        logic_combobox.currentIndexChanged.connect(self.on_value_changed)
        logic_combobox.clearFocus()
        self.set_custom_widget(logic_combobox)

    def set_custom_widget(self, widget):
        if self.widget():
            raise Exception("Custom node widget already set.")
        group = GroupWidget(self.label)
        group.add_node_widget(widget)
        self.setWidget(group)

    def get_value(self):
        combo_widget = self.get_custom_widget()
        return str(combo_widget.currentText())

    def set_value(self, text=''):
        combo_widget = self.get_custom_widget()
        if type(text) is list:
            combo_widget.clear()
            combo_widget.addItems(text)
            return
        if text != self.get_value():
            index = combo_widget.findText(text, Qt.MatchExactly)
            combo_widget.setCurrentIndex(index)

    def add_item(self, item):
        combo_widget = self.get_custom_widget()
        combo_widget.addItem(item)

    def add_items(self, items=None):
        if items:
            combo_widget = self.get_custom_widget()
            combo_widget.addItems(items)

    def all_items(self):
        combo_widget = self.get_custom_widget()
        return [combo_widget.itemText(i) for i in range(combo_widget.count())]

    def sort_items(self):
        items = sorted(self.all_items())
        combo_widget = self.get_custom_widget()
        combo_widget.clear()
        combo_widget.addItems(items)

    def clear(self):
        combo_widget = self.get_custom_widget()
        combo_widget.clear()


class TruthWidget(BaseWidget):
    def __init__(self, parent=None):
        super(TruthWidget, self).__init__(parent)
        # new checkbox
        truth_checkbox = QCheckBox("Truth")
        truth_checkbox.setChecked(True)
        truth_checkbox.setMinimumWidth(80)
        truth_checkbox.setStyleSheet(STYLE_QCHECKBOX)

        # set font
        font = truth_checkbox.font()
        font.setPointSize(8)
        truth_checkbox.setFont(font)

        # blind to groupbox
        self.set_custom_widget(truth_checkbox)
        self.widget().setMaximumWidth(140)

    def get_value(self):
        return self.get_custom_widget().isChecked()

    def set_value(self, state=False):
        if state != self.get_value():
            self.get_custom_widget().setChecked(state)


class ConstituteWidget(BaseWidget):
    def __init__(self, parent=None):
        super(ConstituteWidget, self).__init__(parent)
        constitute_textedit = QTextEdit()
        constitute_textedit.setStyleSheet(STYLE_QTEXTEDIT)
        constitute_textedit.setAlignment(Qt.AlignLeft)
        constitute_textedit.clearFocus()
        constitute_textedit.resize(60, 60)
        self.set_custom_widget(constitute_textedit)

    def get_value(self):
        return str(self.get_custom_widget().text())

    def set_value(self, text=''):
        if text != self.get_value():
            self.get_custom_widget().setText(text)


class NodeNameValidator(QRegExpValidator):
    def __init__(self, parent=None):
        super(NodeNameValidator, self).__init__(QRegExp('^[a-zA-Z][a-zA-Z0-9_ ]*$'), parent)


class InputTextField(QGraphicsTextItem):
    edit_finished = pyqtSignal(bool)
    start_editing = pyqtSignal()

    def __init__(self, text, node, parent=None, single_line=False, validator=None):
        super(InputTextField, self).__init__(text, parent)
        self.node = node
        self.single_line = single_line
        self.validator = validator
        self.text_before_editing = ""
        self.origMoveEvent = self.mouseMoveEvent
        self.mouseMoveEvent = self.node.mouseMoveEvent
        # SET BASIC FUNCTION
        self.basic_function()

    def basic_function(self):
        self.setFlags(QGraphicsWidget.ItemSendsGeometryChanges | QGraphicsWidget.ItemIsSelectable)
        self.setObjectName("Nothing")

    def keyPressEvent(self, event) -> None:
        # insert key text into text field.
        current_key = event.key()
        if self.validator is not None:
            key_button_text = event.text()
            doc = QTextDocument(self.document().toPlainText())
            selected_text = self.textCursor().selectedText()
            cursor = doc.find(selected_text)
            cursor.insertText(key_button_text)
            future_text = doc.toPlainText()
            validator_state, chunk, pos = self.validator.validate(future_text, 0)
            if current_key not in (Qt.Key_Backspace, Qt.Key_Delete):
                if validator_state == QValidator.Invalid:
                    return

        # restore text before editing and return.
        if current_key == Qt.Key_Escape:
            self.setPlainText(self.text_before_editing)
            self.clearFocus()
            super(InputTextField, self).keyPressEvent(event)
            return

        # once press enter or return, it will not wrap around
        if self.single_line:
            if current_key in (Qt.Key_Return, Qt.Key_Enter):
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
        self.setFlag(QGraphicsWidget.ItemIsFocusable, True)
        self.start_editing.emit()
        self.setFocus()

    def focusInEvent(self, event) -> None:
        # todo: disable shortcuts in view
        # start editing and disable to changed focus into node
        self.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.setObjectName("MouseLocked")
        self.text_before_editing = self.toPlainText()
        self.mouseMoveEvent = self.origMoveEvent
        super(InputTextField, self).focusInEvent(event)

    def focusOutEvent(self, event) -> None:
        # todo: enable shortcuts in view
        # clear selection
        cursor = self.textCursor()
        cursor.clearSelection()
        self.setTextCursor(cursor)
        super(InputTextField, self).focusOutEvent(event)
        self.setTextInteractionFlags(Qt.NoTextInteraction)
        self.setObjectName("Nothing")
        if self.toPlainText() == "" and self.validator is not None:
            self.setPlainText(self.text_before_editing)
            self.edit_finished.emit(False)
        else:
            self.edit_finished.emit(True)
        self.mouseMoveEvent = self.node.mouseMoveEvent

    def setGeometry(self, rect):
        self.prepareGeometryChange()
        self.setPos(rect.topLeft())


class NodeNameWidget(QGraphicsWidget):
    def __init__(self, parent=None):
        super(NodeNameWidget, self).__init__(parent)
        # SET BASIC FUNCTION
        # todo: set parent name
        self.label_item = InputTextField(self.parentItem().name, parent, self,
                                         single_line=True, validator=NodeNameValidator())
        self.label_font = QFont("Consolas")
        self.hovered = False
        self.base_function()

    def base_function(self):
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsWidget.ItemSendsGeometryChanges)
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        # todo: set parent label color
        # self.label_item.setDefaultTextColor(self.parentItem().label_item_color)
        self.label_item.setAcceptHoverEvents(True)
        # todo: set parent shape
        self.label_item.document().contentsChanged.connect(self.parentItem().update_node_shape)
        # todo: set finalize rename
        # self.label_item.edit_finished.connect(self.parentItem().finalize_rename)
        self.label_item.hoverMoveEvent = self.hoverMoveEvent

        self.label_font.setPointSize(6)
        self.setGraphicsItem(self.label_item)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

    def set_html(self, html):
        self.prepareGeometryChange()
        self.label_item.setHtml(html)
        self.updateGeometry()
        self.update()

    def hoverEnterEvent(self, event) -> None:
        super(NodeNameWidget, self).hoverEnterEvent(event)
        self.hovered = True
        self.update()

    def hoverMoveEvent(self, event) -> None:
        self.parentItem().hoverMoveEvent(event)

    def hoverLeaveEvent(self, event) -> None:
        self.hovered = False
        self.update()

    def sizeHint(self, which=None, constraint=None) -> QtCore.QSizeF:
        width = QFontMetrics(self.label_item.font()).width(self.label_item.toPlainText())
        height = self.label_item.boundingRect().height() + 5
        return QSizeF(width, height)


class Node(QGraphicsWidget):
    display_name_changed = pyqtSignal(str)
    draw_label = None

    def __init__(self):
        super(Node, self).__init__()
        # SET BASIC FUNCTION.
        self.name = "Default NodeName"
        self.basic_function()

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
        #   HEADER LAYOUT
        self.header_layout = QGraphicsLinearLayout(Qt.Horizontal)
        self.header_layout_margins = 0
        self.header_layout_spacing = 3
        self.gui_layout()

        self.setLayout(self.node_layout)
        self.node_name = NodeNameWidget(self)
        self.node_layout.addItem(self.node_name)
        self.node_layout.addItem(TestWidget("hello", self))

        # RESIZE
        self.resizing = False

    def basic_function(self):
        self.setFlags(QGraphicsWidget.ItemIsMovable | QGraphicsWidget.ItemIsSelectable |
                      QGraphicsWidget.ItemIsFocusable | QGraphicsWidget.ItemSendsGeometryChanges)
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setAcceptHoverEvents(True)
        self.setZValue(Z_VAL_NODE)

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
        painter.restore()

    def gui_layout(self):
        self.node_layout.setContentsMargins(self.node_layout_margins, self.node_layout_margins,
                                            self.node_layout_margins, self.node_layout_margins)
        self.node_layout.setSpacing(self.node_layout_spacing)

    def update_node_shape(self):
        self.prepareGeometryChange()
        self.node_layout.invalidate()
        self.updateGeometry()
        self.update()
        self.node_name.updateGeometry()
        self.node_name.update()

    def mousePressEvent(self, event) -> None:
        if event.modifiers() & Qt.ShiftModifier:
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
