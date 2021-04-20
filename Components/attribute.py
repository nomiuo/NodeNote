from PyQt5 import QtCore, QtWidgets, QtGui
from Model import constants, stylesheet
from Components import port


__all__ = ["NodeNameWidget", "NodeNameValidator", "InputTextField", "LogicWidget", "TruthWidget"]


class NodeNameValidator(QtGui.QRegExpValidator):
    def __init__(self, parent=None):
        super(NodeNameValidator, self).__init__(QtCore.QRegExp('^[a-zA-Z][a-zA-Z0-9_ ]*$'), parent)


class InputTextField(QtWidgets.QGraphicsTextItem):
    edit_finished = QtCore.pyqtSignal(bool)
    start_editing = QtCore.pyqtSignal()

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
        self.setFlags(QtWidgets.QGraphicsWidget.ItemSendsGeometryChanges | QtWidgets.QGraphicsWidget.ItemIsSelectable)
        self.setObjectName("Nothing")

    def keyPressEvent(self, event) -> None:
        # insert key text into text field.
        current_key = event.key()
        if self.validator is not None:
            key_button_text = event.text()
            doc = QtGui.QTextDocument(self.document().toPlainText())
            selected_text = self.textCursor().selectedText()
            cursor = doc.find(selected_text)
            cursor.insertText(key_button_text)
            future_text = doc.toPlainText()
            validator_state, chunk, pos = self.validator.validate(future_text, 0)
            if current_key not in (QtCore.Qt.Key_Backspace, QtCore.Qt.Key_Delete):
                if validator_state == QtGui.QValidator.Invalid:
                    return

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
        # todo: disable shortcuts in view
        # start editing and disable to changed focus into node
        self.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
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
        self.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
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


class NodeNameWidget(QtWidgets.QGraphicsWidget):
    def __init__(self, parent=None):
        super(NodeNameWidget, self).__init__(parent)
        # SET BASIC FUNCTION
        # todo: set parent name
        self.label_item = InputTextField(self.parentItem().name, parent, self,
                                         single_line=True, validator=NodeNameValidator())
        self.label_font = QtGui.QFont("Consolas")
        self.hovered = False
        self.base_function()

    def base_function(self):
        self.setAcceptHoverEvents(True)
        self.setFlag(QtWidgets.QGraphicsWidget.ItemSendsGeometryChanges)
        self.setCacheMode(QtWidgets.QGraphicsItem.DeviceCoordinateCache)
        self.label_item.setAcceptHoverEvents(True)
        self.label_item.document().contentsChanged.connect(self.parentItem().update_node_shape)
        self.label_item.hoverMoveEvent = self.hoverMoveEvent

        self.label_font.setPointSize(6)
        self.setGraphicsItem(self.label_item)
        self.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)

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
        width = QtGui.QFontMetrics(self.label_item.font()).width(self.label_item.toPlainText())
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


class LogicWidget(QtWidgets.QGraphicsWidget):
    # todo :set layout
    def __init__(self, scene, parent=None):
        super(LogicWidget, self).__init__(parent)
        self.resizing = False
        self.scene = scene
        self.setFlags(QtWidgets.QGraphicsItem.ItemIsMovable | QtWidgets.QGraphicsItem.ItemIsSelectable)
        self.input_port = port.Port(constants.INPUT_NODE_TYPE, self)
        self.output_port = port.Port(constants.OUTPUT_NODE_TYPE, self)
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
        proxywidget.setParentItem(self)
        self.resize(proxywidget.size().width(), proxywidget.size().height())

    def get_value(self):
        combo_widget = self.get_custom_widget()
        return str(combo_widget.currentText())

    def paint(self, painter, option, widget=None) -> None:
        super(LogicWidget, self).paint(painter, option, widget)
        self.input_port.setPos(-12, self.size().height() / 2 - 3)
        self.output_port.setPos(self.size().width() - 12, self.size().height() / 2 - 3)

        painter.setPen(QtGui.QPen(QtGui.QColor(15, 242, 254, 255), 5))
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawRoundedRect(0, 0, self.size().width(), self.size().height(), 2, 2)

        self.childItems()[0].widget().resize(self.size().width(), self.size().height())

    def mousePressEvent(self, event) -> None:
        if int(event.modifiers()) & QtCore.Qt.ShiftModifier and type(self.scene.itemAt(event)) in constants.SCALE_WIDGET:
            self.resizing = True
            self.setCursor(QtCore.Qt.SizeAllCursor)
        else:
            super(LogicWidget, self).mousePressEvent(event)

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
                print(current_width, current_height)
        else:
            super(LogicWidget, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        if self.resizing:
            self.resizing = False
            self.setCursor(QtCore.Qt.ArrowCursor)
        else:
            super(LogicWidget, self).mouseReleaseEvent(event)


class TruthWidget(QtWidgets.QGraphicsProxyWidget):
    def __init__(self, parent=None):
        super(TruthWidget, self).__init__(parent)
        # new checkbox
        truth_checkbox = QtWidgets.QCheckBox("Truth")
        truth_checkbox.setChecked(True)
        truth_checkbox.setMinimumWidth(80)
        truth_checkbox.setStyleSheet(stylesheet.STYLE_QCHECKBOX)

        # set font
        font = truth_checkbox.font()
        font.setPointSize(8)
        truth_checkbox.setFont(font)

        # blind to groupbox
        self.set_custom_widget(truth_checkbox)

    def get_value(self):
        return self.get_custom_widget().isChecked()

    def set_value(self, state=False):
        if state != self.get_value():
            self.get_custom_widget().setChecked(state)

