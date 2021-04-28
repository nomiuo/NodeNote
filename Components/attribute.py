from PyQt5 import QtCore, QtWidgets, QtGui
from Model import constants, stylesheet
from Components import port

import os


__all__ = ["SubConstituteWidget", "InputTextField",
           "LogicWidget", "TruthWidget", "AttributeWidget"]


class PythonHighlighter(QtGui.QSyntaxHighlighter):
    rules = []

    def __init__(self, parent=None):
        super(PythonHighlighter, self).__init__(parent)
        # KEYWORD
        # format
        keyword_format = QtGui.QTextCharFormat()
        keyword_format.setForeground(QtCore.Qt.darkBlue)
        keyword_format.setFontWeight(QtGui.QFont.Bold)
        # pattern
        keyword_pattern = [r"\band\b", r"\bas\b", r"\bassert\b", r"\bbreak\b", r"\bclass\b", r"\bcontinue\b",
                           r"\bdef\b", r"\belif\b", r"\bdel\b", r"\belse\b", r"\bexcept\b", r"\bFalse\b",
                           r"\bfinally\b", r"\b@staticmethod\b",
                           r"\bfor\b", r"\bfrom\b", r"\bglobal\b", r"\bif\b", r"\bimport\b", r"\bin\b", r"\bis\b",
                           r"\blambda\b", r"\bNone\b", r"\bnonlocal\b", r"\bnot\b", r"\bor\b", r"\bpass\b",
                           r"\braise\b", r"\breturn\b", r"\bTrue\b", r"\bwhile\b", r"\bwith\b", r"\byield\b"]
        for pattern in keyword_pattern:
            PythonHighlighter.rules.append((QtCore.QRegExp(pattern), keyword_format))
        # COMMENT
        # format
        comment_format = QtGui.QTextCharFormat()
        comment_format.setForeground(QtGui.QColor(0, 127, 0))
        comment_format.setFontItalic(True)
        # pattern
        PythonHighlighter.rules.append((QtCore.QRegExp(r"#.*"), comment_format))
        # STRING
        # format
        string_format = QtGui.QTextCharFormat()
        string_format.setForeground(QtCore.Qt.darkYellow)
        # pattern
        string_pattern = QtCore.QRegExp(r"""(?:'[^']*''|"[^"]*")""")
        string_pattern.setMinimal(True)
        PythonHighlighter.rules.append((string_pattern, string_format))
        string_pattern = QtCore.QRegExp(r"""(:?"["]".*"["]"|'''.*''')""")
        string_pattern.setMinimal(True)
        PythonHighlighter.rules.append((string_pattern, string_format))
        # PYTHON
        self.distinguish_python_first = QtCore.QRegExp(r"""```python""")
        self.distinguish_python_last = QtCore.QRegExp(r"""``(?!`)""")

    def highlightBlock(self, text: str) -> None:
        DISTINGUISH = 1
        NONE = 2
        # DISTINGUISH PYTHON
        first_i = self.distinguish_python_first.indexIn(text)
        last_i = self.distinguish_python_last.indexIn(text)
        if constants.DEBUG_PYTHON_SYNTAXHIGHTLIGHTER:
            print(first_i, last_i, self.currentBlockState())
        if self.previousBlockState() == DISTINGUISH and first_i == -1 and last_i == -1:
            # NORMAL HIGHLIGHT
            for regex, format in PythonHighlighter.rules:
                normal_i = regex.indexIn(text)
                while normal_i >= 0:
                    length = regex.matchedLength()
                    self.setFormat(normal_i, length, format)
                    normal_i = regex.indexIn(text, normal_i + length)
            self.setCurrentBlockState(DISTINGUISH)
        elif first_i == 0 and last_i == 1:
            self.setCurrentBlockState(DISTINGUISH)
        elif last_i > -1:
            self.setCurrentBlockState(NONE)
        else:
            self.setCurrentBlockState(NONE)


class InputTextField(QtWidgets.QGraphicsTextItem):
    edit_finished = QtCore.pyqtSignal(bool)
    start_editing = QtCore.pyqtSignal()

    def __init__(self, text, node, parent=None, single_line=False):
        super(InputTextField, self).__init__(text, parent)
        # BASIC SETTINGS
        self.setFlags(QtWidgets.QGraphicsWidget.ItemSendsGeometryChanges | QtWidgets.QGraphicsWidget.ItemIsSelectable)
        self.setOpenExternalLinks(True)
        self.setObjectName("Nothing")
        self.node = node
        self.single_line = single_line
        self.text_before_editing = ""
        self.origMoveEvent = self.mouseMoveEvent
        self.mouseMoveEvent = self.node.mouseMoveEvent
        # DOCUMENT SETTINGS

    @staticmethod
    def add_table(cursor):
        # create parameters
        table_format = QtGui.QTextTableFormat()

        # set and insert
        table_format.setCellPadding(10)
        table_format.setCellSpacing(2)
        table_format.setAlignment(QtCore.Qt.AlignCenter)
        table_format.setBackground(QtGui.QBrush(QtGui.QColor(229, 255, 255, 255)))
        cursor.insertTable(1, 1, table_format)

    @staticmethod
    def table_insert_column(table, cursor):
        column = table.cellAt(cursor).column() + 1
        table.insertColumns(column, 1)

    @staticmethod
    def table_insert_row(table, cursor):
        row = table.cellAt(cursor).row() + 1
        table.insertRows(row, 1)

    @staticmethod
    def table_delete_column(table, cursor):
        column = table.cellAt(cursor).column()
        table.removeColumns(column, 1)

    @staticmethod
    def table_delete_row(table, cursor):
        row = table.cellAt(cursor).row()
        table.removeRows(row, 1)

    @staticmethod
    def add_list(cursor):
        # create parameters
        list_format = QtGui.QTextListFormat()

        # set and insert
        list_format.setIndent(4)
        list_format.setStyle(QtGui.QTextListFormat.ListDecimal)
        cursor.insertList(list_format)

    @staticmethod
    def add_openlink(cursor):
        # create parameters
        pass

    @staticmethod
    def add_codeblock(cursor):
        codeblock_format = QtGui.QTextFrameFormat()
        codeblock_format.setBorder(5)
        codeblock_format.setPadding(10)
        codeblock_format.setBackground(QtGui.QBrush(QtGui.QColor(229, 255, 255)))
        cursor.insertFrame(codeblock_format)

    @staticmethod
    def paste(document, cursor):
        mime_data = QtWidgets.QApplication.clipboard().mimeData()
        if mime_data.hasImage():
            image = QtGui.QImage(mime_data.imageData())
            cursor.insertImage(image)
        elif mime_data.hasUrls():
            for u in mime_data.urls():
                file_ext = os.path.splitext(str(u.toLocalFile()))[1].lower()
                print(file_ext, u.isLocalFile())
                if u.isLocalFile() and file_ext in ('.jpg', '.png', '.bmp', '.icon', '.jpeg'):
                    cursor.insertImage(u.toLocalFile())
                else:
                    break
            else:
                return
        elif mime_data.hasText():
            mime_data.setData("text/plain", QtCore.QByteArray())
            text = mime_data.text()
            cursor.insertText(text)

    def keyPressEvent(self, event) -> None:
        # insert key text into text field.
        current_key = event.key()
        current_cursor = self.textCursor()

        # restore text before editing and return.
        if current_key == QtCore.Qt.Key_Escape:
            self.clearFocus()
            super(InputTextField, self).keyPressEvent(event)
            return

        # todo: anchor and open link
        # todo: tab selected text
        # todo: delete "\n" before list
        # todo: delete codeblock
        # once press enter or return, it will not wrap around
        if self.single_line:
            if current_key in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
                if self.toPlainText() == "":
                    self.setHtml(self.text_before_editing)
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

        # table operation
        current_table = current_cursor.currentTable()
        if current_key == QtCore.Qt.Key_1 and event.modifiers() & QtCore.Qt.ControlModifier:
            self.add_table(current_cursor)
        if current_key == QtCore.Qt.Key_T and event.modifiers() & QtCore.Qt.ControlModifier and current_table:
            self.table_insert_column(current_table, current_cursor)
        if current_key == QtCore.Qt.Key_R and event.modifiers() & QtCore.Qt.ControlModifier and current_table:
            self.table_insert_row(current_table, current_cursor)
        if current_key == QtCore.Qt.Key_D and event.modifiers() & QtCore.Qt.ControlModifier and current_table:
            self.table_delete_column(current_table, current_cursor)
        if current_key == QtCore.Qt.Key_F and event.modifiers() & QtCore.Qt.ControlModifier and current_table:
            self.table_delete_row(current_table, current_cursor)

        # list operation
        if current_key == QtCore.Qt.Key_2 and event.modifiers() & QtCore.Qt.ControlModifier:
            self.add_list(current_cursor)

        # open link
        if current_key == QtCore.Qt.Key_3 and event.modifiers() & QtCore.Qt.ControlModifier:
            self.add_openlink(current_cursor)

        # code
        if current_key == QtCore.Qt.Key_4 and event.modifiers() & QtCore.Qt.ControlModifier:
            self.add_codeblock(current_cursor)

    def sceneEvent(self, event: QtCore.QEvent) -> bool:
        if event.type() == QtCore.QEvent.KeyPress:
            if event.matches(QtGui.QKeySequence.Paste):
                self.paste(self.document(), self.textCursor())
                return False
            elif event.key() == QtCore.Qt.Key_Tab:
                self.textCursor().insertText("    ")
                return False
            else:
                super(InputTextField, self).sceneEvent(event)
                return False
        else:
            super(InputTextField, self).sceneEvent(event)
            return False

    def mousePressEvent(self, event) -> None:
        # change focus into node
        if self.objectName() == "MouseLocked":
            super(InputTextField, self).mousePressEvent(event)
        else:
            self.node.mousePressEvent(event)
            self.clearFocus()

    def contextMenuEvent(self, event: 'QtWidgets.QGraphicsSceneContextMenuEvent') -> None:
        # not implementing, debug for right mouse clicked
        pass

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
        self.text_before_editing = self.toHtml()
        self.mouseMoveEvent = self.origMoveEvent
        super(InputTextField, self).focusInEvent(event)

    def focusOutEvent(self, event) -> None:
        # clear selection
        super(InputTextField, self).focusOutEvent(event)
        self.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.setObjectName("Nothing")
        if self.toHtml() == "":
            self.setHtml(self.text_before_editing)
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
        self.label_item.setAcceptHoverEvents(True)
        self.label_item.document().contentsChanged.connect(self.parentItem().text_change_node_shape)
        self.label_item.hoverMoveEvent = self.hoverMoveEvent
        self.label_font = QtGui.QFont("Lucida MAC")
        self.label_font.setPointSize(8)
        self.label_item.setFont(self.label_font)

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
        layout = QtWidgets.QVBoxLayout(self)
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
    def __init__(self, truth=True, parent=None):
        super(TruthWidget, self).__init__(parent)
        # new checkbox
        self.truth_checkbox = QtWidgets.QCheckBox("Truth")
        self.truth_checkbox.setChecked(truth)
        self.truth_checkbox.setStyleSheet(stylesheet.STYLE_QCHECKBOX)

        # set font
        font = self.truth_checkbox.font()
        font.setPointSize(8)
        self.truth_checkbox.setFont(font)

        # add into group
        proxywidget = QtWidgets.QGraphicsProxyWidget()
        proxywidget.setWidget(self.truth_checkbox)
        self.layout = QtWidgets.QGraphicsLinearLayout(QtCore.Qt.Horizontal)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addItem(proxywidget)
        self.setLayout(self.layout)

    def sizeHint(self, which=None, constraint=None) -> QtCore.QSizeF:
        width = self.truth_checkbox.width() + 5
        height = self.truth_checkbox.height() + 5
        return QtCore.QSizeF(width, height)

    def boundingRect(self) -> QtCore.QRectF:
        return QtCore.QRectF(0, 0,
                             self.truth_checkbox.width() + 5,
                             self.truth_checkbox.height() + 5)


class AttributeWidget(QtWidgets.QGraphicsWidget):
    display_name_changed = QtCore.pyqtSignal(str)
    draw_label = None

    def __init__(self):
        super(AttributeWidget, self).__init__()
        # SET BASIC FUNCTION.
        self.name = "Default Attribute Name"
        self.setFlags(QtWidgets.QGraphicsWidget.ItemIsSelectable | QtWidgets.QGraphicsWidget.ItemIsFocusable |
                      QtWidgets.QGraphicsWidget.ItemSendsGeometryChanges)
        self.setCacheMode(QtWidgets.QGraphicsItem.DeviceCoordinateCache)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setAcceptHoverEvents(True)
        self.setZValue(constants.Z_VAL_NODE)

        # COLORS
        self.color = (229, 255, 255, 125)
        self.border_color = (46, 57, 66, 255)
        self.selected_color = (255, 255, 255, 30)
        self.selected_border_color = (254, 207, 42, 255)

        # LAYOUTS
        #   create
        self.layout = QtWidgets.QGraphicsLinearLayout(QtCore.Qt.Horizontal)
        self.input_layout = QtWidgets.QGraphicsLinearLayout(QtCore.Qt.Vertical)
        self.output_layout = QtWidgets.QGraphicsLinearLayout(QtCore.Qt.Vertical)
        self.attribute_layout = QtWidgets.QGraphicsLinearLayout(QtCore.Qt.Vertical)
        self.attribute_settings_layout = QtWidgets.QGraphicsLinearLayout(QtCore.Qt.Horizontal)
        #   sapcing
        self.layout.setSpacing(0)
        self.input_layout.setSpacing(0)
        self.output_layout.setSpacing(0)
        self.attribute_layout.setSpacing(0)
        self.attribute_settings_layout.setSpacing(0)
        #   margin
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.input_layout.setContentsMargins(0, 0, 0, 0)
        self.output_layout.setContentsMargins(0, 0, 0, 0)
        self.attribute_layout.setContentsMargins(0, 0, 0, 0)
        self.attribute_settings_layout.setContentsMargins(0, 0, 0, 0)

        # WIDGETS
        #   title name widget
        self.attribute_widget = SubConstituteWidget(self)
        #   title setting widget
        #       align
        self.align_left = QtGui.QPixmap("Resources/TextSettings/left.png")
        self.align_left_widget = QtWidgets.QGraphicsWidget()
        self.align_left_widget.setMaximumSize(20.0, 20.0)
        self.align_left_widget.setMinimumSize(20.0, 20.0)
        palette = self.align_left_widget.palette()
        palette.setBrush(QtGui.QPalette.Window, QtGui.QBrush(self.align_left))
        self.align_left_widget.setAutoFillBackground(True)
        self.align_left_widget.setPalette(palette)

        self.align_center = QtGui.QPixmap("Resources/TextSettings/center.png")
        self.align_center_widget = QtWidgets.QGraphicsWidget()
        self.align_center_widget.setMaximumSize(20.0, 20.0)
        self.align_center_widget.setMinimumSize(20.0, 20.0)
        palette = self.align_center_widget.palette()
        palette.setBrush(QtGui.QPalette.Window, QtGui.QBrush(self.align_center))
        self.align_center_widget.setAutoFillBackground(True)
        self.align_center_widget.setPalette(palette)

        self.align_right = QtGui.QPixmap("Resources/TextSettings/right.png")
        self.align_right_widget = QtWidgets.QGraphicsWidget()
        self.align_right_widget.setMaximumSize(20.0, 20.0)
        self.align_right_widget.setMinimumSize(20.0, 20.0)
        palette = self.align_right_widget.palette()
        palette.setBrush(QtGui.QPalette.Window, QtGui.QBrush(self.align_right))
        self.align_right_widget.setAutoFillBackground(True)
        self.align_right_widget.setPalette(palette)
        #       setting
        self.attribute_setting_pic = QtGui.QPixmap("Resources/TextSettings/attribute_setting_img.png")
        self.attribute_setting_widget = QtWidgets.QGraphicsWidget()
        self.attribute_setting_widget.setMaximumSize(20.0, 20.0)
        self.attribute_setting_widget.setMinimumSize(20.0, 20.0)
        palette = self.attribute_setting_widget.palette()
        palette.setBrush(QtGui.QPalette.Window, QtGui.QBrush(self.attribute_setting_pic))
        self.attribute_setting_widget.setAutoFillBackground(True)
        self.attribute_setting_widget.setPalette(palette)
        #   port widgets
        self.true_input_port = port.Port(constants.INPUT_NODE_TYPE, self)
        self.true_output_port = port.Port(constants.OUTPUT_NODE_TYPE, self)
        self.false_input_port = port.Port(constants.INPUT_NODE_TYPE, self)
        self.false_output_port = port.Port(constants.OUTPUT_NODE_TYPE, self)
        self.true_input_port.setMaximumSize(25, 25)
        self.true_input_port.setMinimumSize(25, 25)
        self.true_output_port.setMaximumSize(25, 25)
        self.true_output_port.setMinimumSize(25, 25)
        self.false_input_port.setMaximumSize(25, 25)
        self.false_input_port.setMinimumSize(25, 25)
        self.false_output_port.setMaximumSize(25, 25)
        self.false_output_port.setMinimumSize(25, 25)
        # IMPLEMENT WIDGETS
        #   layout
        self.setLayout(self.layout)
        self.layout.addItem(self.input_layout)
        self.layout.addStretch(1)
        self.layout.addItem(self.attribute_layout)
        self.layout.addStretch(1)
        self.layout.addItem(self.output_layout)
        #  input layout
        self.input_layout.addItem(self.true_input_port)
        self.input_layout.addStretch(1)
        self.input_layout.addItem(self.false_input_port)
        # attribute layout
        self.attribute_layout.addItem(self.attribute_settings_layout)
        self.attribute_layout.addItem(self.attribute_widget)
        self.attribute_layout.setAlignment(self.attribute_settings_layout, QtCore.Qt.AlignCenter)
        self.attribute_layout.setAlignment(self.attribute_widget, QtCore.Qt.AlignCenter)
        self.attribute_settings_layout.addItem(self.align_left_widget)
        self.attribute_settings_layout.addItem(self.align_center_widget)
        self.attribute_settings_layout.addItem(self.align_right_widget)
        self.attribute_settings_layout.addItem(self.attribute_setting_widget)
        # output layout
        self.output_layout.addItem(self.true_output_port)
        self.output_layout.addStretch(1)
        self.output_layout.addItem(self.false_output_port)

        # RESIZE
        self.resizing = False

    def paint(self, painter, option, widget=None) -> None:
        painter.save()

        # draw border
        bg_border = 1.0
        radius = 2
        rect = QtCore.QRectF(
            0.5 - (bg_border / 2),
            0.5 - (bg_border / 2),
            self.boundingRect().width() + bg_border,
            self.boundingRect().height() + bg_border
        )
        border_color = QtGui.QColor(*self.border_color)
        path = QtGui.QPainterPath()
        path.addRoundedRect(rect, radius, radius)

        # draw background
        rect = self.boundingRect()
        painter.setBrush(QtGui.QColor(*self.color) if not self.isSelected() else QtGui.QColor(*self.selected_color))
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRoundedRect(rect, radius, radius)

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

        painter.restore()

    def text_change_node_shape(self):
        # text
        self.attribute_widget.updateGeometry()
        self.attribute_widget.update()
        #  layout
        self.prepareGeometryChange()
        self.layout.invalidate()
        self.layout.activate()
        self.updateGeometry()
        self.update()
        self.attribute_layout.updateGeometry()
        self.attribute_layout.invalidate()

    def mouse_update_node_size(self, event):
        if event.type() == QtCore.QEvent.GraphicsSceneMousePress and not self.parentItem():
            self.resizing = True
            self.setCursor(QtCore.Qt.SizeAllCursor)
        elif event.type() == QtCore.QEvent.GraphicsSceneMouseRelease and not self.parentItem():
            self.resizing = False
            self.setCursor(QtCore.Qt.ArrowCursor)
        elif event.type() == QtCore.QEvent.GraphicsSceneMouseMove and not self.parentItem():
            past_pos = self.scenePos()
            past_width = self.size().width()
            past_height = self.size().height()
            current_pos = self.mapToScene(event.pos())
            current_width = current_pos.x() - past_pos.x() if current_pos.x() >= past_pos.x() else past_width
            current_height = current_pos.y() - past_pos.y() if current_pos.y() >= past_pos.y() else past_height
            self.resize(current_width, current_height)

            if constants.DEBUG_TUPLE_NODE_SCALE:
                print(current_width, current_height)

    def get_port_position(self, port_type):
        # todo: wrong
        x = -10 if port_type == constants.INPUT_NODE_TYPE else self.size().width() - 10
        y = self.size().height() / 2
        return x, y

    def add_subwidget(self):
        subwidget = AttributeWidget()
        self.attribute_layout.addItem(subwidget)

    def mousePressEvent(self, event) -> None:
        if int(event.modifiers()) & QtCore.Qt.ShiftModifier:
            self.mouse_update_node_size(event)
        elif self.scene().itemAt(self.mapToScene(event.pos()), QtGui.QTransform()) is self.align_left_widget:
            cursor = self.attribute_widget.label_item.textCursor()
            frame = self.attribute_widget.label_item.document().rootFrame()
            if cursor.hasSelection():
                format = QtGui.QTextBlockFormat()
                format.setAlignment(QtCore.Qt.AlignLeft)
                start_pos = cursor.selectionStart()
                end_pos = cursor.selectionEnd()
                print(start_pos, end_pos)
                it = frame.begin()
                while it != frame.end():
                    child_frame = it.currentFrame()
                    child_block = it.currentBlock()
                    print(child_block, child_block)
                    it += 1

                cursor.select(QtGui.QTextCursor.BlockUnderCursor)
                cursor.mergeBlockFormat(format)
                cursor.clearSelection()
                self.attribute_widget.label_item.setTextCursor(cursor)
        elif self.scene().itemAt(self.mapToScene(event.pos()), QtGui.QTransform()) is self.align_center_widget:
            print("hello")
        elif self.scene().itemAt(self.mapToScene(event.pos()), QtGui.QTransform()) is self.align_right_widget:
            print("hello")
        else:
            super(AttributeWidget, self).mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:
        if self.resizing:
            self.mouse_update_node_size(event)
        else:
            super(AttributeWidget, self).mouseMoveEvent(event)
        if not self.parentItem():
            self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        else:
            self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, False)

    def mouseReleaseEvent(self, event) -> None:
        if self.resizing:
            self.mouse_update_node_size(event)
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
