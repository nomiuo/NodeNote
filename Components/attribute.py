import re
import os
import io

import validators
import matplotlib.pyplot as plt
import pylab
import numpy as np
from PyQt5 import QtCore, QtWidgets, QtGui
from Model import constants, stylesheet
from Components import port

__all__ = ["SubConstituteWidget", "InputTextField",
           "LogicWidget", "TruthWidget", "AttributeWidget"]


class SizeDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(SizeDialog, self).__init__(parent)
        self.resize(100, 80)
        self.setWindowTitle("Set Image Width and Height")
        self.setWindowIcon(QtGui.QIcon("Resources/Dialog_icon/Plane.png"))

        self.num_width = QtWidgets.QLineEdit(parent=self)
        self.num_width.setValidator(QtGui.QDoubleValidator())
        self.num_height = QtWidgets.QLineEdit(parent=self)
        self.num_height.setValidator(QtGui.QDoubleValidator())
        grid = QtWidgets.QGridLayout()
        grid.addWidget(QtWidgets.QLabel("Width: ", parent=self), 0, 0, 1, 1)
        grid.addWidget(QtWidgets.QLabel("Height: ", parent=self), 1, 0, 1, 1)
        grid.addWidget(self.num_width, 0, 1, 1, 1)
        grid.addWidget(self.num_height, 1, 1, 1, 1)

        button_box = QtWidgets.QDialogButtonBox(parent=self)
        button_box.setOrientation(QtCore.Qt.Horizontal)
        button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel |
                                      QtWidgets.QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(grid)
        spacerItem = QtWidgets.QSpacerItem(20, 48, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        layout.addItem(spacerItem)
        layout.addWidget(button_box)
        self.setLayout(layout)

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, 'Close Message',
                                               "Are you sure to quit?", QtWidgets.QMessageBox.Yes |
                                               QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


def format(color, style=''):
    """Return a QTextCharFormat with the given attributes.
    """
    _color = QtGui.QColor()
    _color.setNamedColor(color)

    _format = QtGui.QTextCharFormat()
    _format.setForeground(_color)
    if 'bold' in style:
        _format.setFontWeight(QtGui.QFont.Bold)
    if 'italic' in style:
        _format.setFontItalic(True)

    return _format


# Syntax styles that can be shared by all languages
STYLES = {
    'keyword': format('blue'),
    'operator': format('red'),
    'brace': format('darkGray'),
    'defclass': format('black', 'bold'),
    'string': format('magenta'),
    'string2': format('darkMagenta'),
    'comment': format('darkGreen', 'italic'),
    'self': format('black', 'italic'),
    'numbers': format('brown'),
}


class PythonHighlighter(QtGui.QSyntaxHighlighter):
    """Syntax highlighter for the Python language.
    """
    # Python keywords
    keywords = [
        'and', 'assert', 'break', 'class', 'continue', 'def',
        'del', 'elif', 'else', 'except', 'exec', 'finally',
        'for', 'from', 'global', 'if', 'import', 'in',
        'is', 'lambda', 'not', 'or', 'pass', 'print',
        'raise', 'return', 'try', 'while', 'yield',
        'None', 'True', 'False',
    ]

    # Python operators
    operators = [
        '=',
        # Comparison
        '==', '!=', '<', '<=', '>', '>=',
        # Arithmetic
        '\+', '-', '\*', '/', '//', '\%', '\*\*',
        # In-place
        '\+=', '-=', '\*=', '/=', '\%=',
        # Bitwise
        '\^', '\|', '\&', '\~', '>>', '<<',
    ]

    # Python braces
    braces = [
        '\{', '\}', '\(', '\)', '\[', '\]',
    ]

    def __init__(self, document):
        QtGui.QSyntaxHighlighter.__init__(self, document)

        # Multi-line strings (expression, flag, style)
        # FIXME: The triple-quotes in these two lines will mess up the
        # syntax highlighting from this point onward
        self.tri_single = (QtCore.QRegExp("'''"), 1, STYLES['string2'])
        self.tri_double = (QtCore.QRegExp('"""'), 2, STYLES['string2'])

        rules = []

        # Keyword, operator, and brace rules
        rules += [(r'\b%s\b' % w, 0, STYLES['keyword'])
                  for w in PythonHighlighter.keywords]
        rules += [(r'%s' % o, 0, STYLES['operator'])
                  for o in PythonHighlighter.operators]
        rules += [(r'%s' % b, 0, STYLES['brace'])
                  for b in PythonHighlighter.braces]

        # All other rules
        rules += [
            # 'self'
            (r'\bself\b', 0, STYLES['self']),

            # Double-quoted string, possibly containing escape sequences
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, STYLES['string']),
            # Single-quoted string, possibly containing escape sequences
            (r"'[^'\\]*(\\.[^'\\]*)*'", 0, STYLES['string']),

            # 'def' followed by an identifier
            (r'\bdef\b\s*(\w+)', 1, STYLES['defclass']),
            # 'class' followed by an identifier
            (r'\bclass\b\s*(\w+)', 1, STYLES['defclass']),

            # From '#' until a newline
            (r'#[^\n]*', 0, STYLES['comment']),

            # Numeric literals
            (r'\b[+-]?[0-9]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, STYLES['numbers']),
        ]

        # Build a QRegExp for each pattern
        self.rules = [(QtCore.QRegExp(pat), index, fmt)
                      for (pat, index, fmt) in rules]

    def highlightBlock(self, text):
        """Apply syntax highlighting to the given block of text.
        """
        # Do other syntax formatting
        for expression, nth, font_format in self.rules:
            index = expression.indexIn(text, 0)

            while index >= 0:
                # We actually want the index of the nth match
                index = expression.pos(nth)
                length = len(expression.cap(nth))
                self.setFormat(index, length, font_format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        # Do multi-line strings
        in_multiline = self.match_multiline(text, *self.tri_single)
        if not in_multiline:
            self.match_multiline(text, *self.tri_double)

    def match_multiline(self, text, delimiter, in_state, style):
        """Do highlighting of multi-line strings. ``delimiter`` should be a
        ``QRegExp`` for triple-single-quotes or triple-double-quotes, and
        ``in_state`` should be a unique integer to represent the corresponding
        state changes when inside those strings. Returns True if we're still
        inside a multi-line string when this function is finished.
        """
        # If inside triple-single quotes, start at 0
        if self.previousBlockState() == in_state:
            start = 0
            add = 0
        # Otherwise, look for the delimiter on this line
        else:
            start = delimiter.indexIn(text)
            # Move past this match
            add = delimiter.matchedLength()

        # As long as there's a delimiter match on this line...
        while start >= 0:
            # Look for the ending delimiter
            end = delimiter.indexIn(text, start + add)
            # Ending delimiter on this line?
            if end >= add:
                length = end - start + add + delimiter.matchedLength()
                self.setCurrentBlockState(0)
            # No; multi-line string
            else:
                self.setCurrentBlockState(in_state)
                length = len(text) - start + add
            # Apply formatting
            self.setFormat(start, length, style)
            # Look for the next match
            start = delimiter.indexIn(text, start + length)

        # Return True if still inside a multi-line string, False otherwise
        if self.currentBlockState() == in_state:
            return True
        else:
            return False


# TODO: edit status to control focus
# TODO: ctrl + c mime data support
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
        # DOCUMNET SETTINGS
        self.document().setIndentWidth(4)
        self.document().setDefaultFont(QtGui.QFont("Inconsolata", 8))
        self.pythonlighter = PythonHighlighter(self.document())
        self.editing_state = False
        self.font_size_editing = True

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
    def add_codeblock(cursor):
        codeblock_format = QtGui.QTextFrameFormat()
        codeblock_format.setBorder(5)
        codeblock_format.setPadding(10)
        codeblock_format.setBackground(QtGui.QBrush(QtGui.QColor(229, 255, 255)))
        cursor.insertFrame(codeblock_format)

    def indent(self):
        cursor = self.textCursor()
        if cursor.hasSelection():
            temp = cursor.blockNumber()
            cursor.setPosition(cursor.anchor())
            diff = cursor.blockNumber() - temp
            direction = QtGui.QTextCursor.Up if diff > 0 else QtGui.QTextCursor.Down
            for _ in range(abs(diff) + 1):
                cursor.movePosition(QtGui.QTextCursor.StartOfLine)
                cursor.insertText("    ")
                cursor.movePosition(direction)
        else:
            cursor.insertText("    ")

    def dedent(self):
        cursor = self.textCursor()
        if cursor.hasSelection():
            temp = cursor.blockNumber()
            cursor.setPosition(cursor.anchor())
            diff = cursor.blockNumber() - temp
            direction = QtGui.QTextCursor.Up if diff > 0 else QtGui.QTextCursor.Down
            for _ in range(abs(diff) + 1):
                cursor.movePosition(QtGui.QTextCursor.StartOfLine)
                line = cursor.block().text()
                if line.startswith("    "):
                    for _ in range(4):
                        cursor.deleteChar()
                else:
                    for char in line[:4]:
                        if char != " ":
                            break
                        cursor.deleteChar()
                cursor.movePosition(direction)
        else:
            cursor.movePosition(QtGui.QTextCursor.StartOfLine)
            line = cursor.block().text()
            if line.startswith("    "):
                for _ in range(4):
                    cursor.deleteChar()
            else:
                for char in line[:4]:
                    if char != " ":
                        break
                    cursor.deleteChar()

    def get_text_maxlength(self):
        document = self.document()
        cursor = self.textCursor()
        cursor.movePosition(QtGui.QTextCursor.Start)
        root = document.rootFrame()
        it = root.begin()
        maxlength = 0
        while it != root.end():
            line_length = self.get_line_length(cursor)
            maxlength = maxlength if maxlength > line_length else line_length
            cursor.movePosition(QtGui.QTextCursor.Down)
            it += 1
        return maxlength

    @staticmethod
    def get_line_length(cursor):
        if constants.DEBUG_RICHTEXT:
            print("cursor postion: ", cursor.position())
        line_type = list()
        for char in cursor.block().text():
            if '\u4e00' <= char <= '\u9fa5':
                line_type.append(1)
                if constants.DEBUG_RICHTEXT:
                    print("Chinese: ", char)
            else:
                line_type.append(0)

        line_position = 0
        line_point = 0
        cursor.movePosition(QtGui.QTextCursor.StartOfLine)
        while not cursor.atBlockEnd():
            point_size = cursor.charFormat().fontPointSize()
            font_point_size = point_size if point_size != 0 else 8
            if line_type[line_position]:
                font_point_size = font_point_size * 2
            line_point += font_point_size
            line_position += 1
            cursor.movePosition(QtGui.QTextCursor.Right, QtGui.QTextCursor.KeepAnchor, 1)
        return line_point

    def align(self, align):
        max_length = self.get_text_maxlength()
        cursor = self.textCursor()
        if align == "Center":
            self.align("Clean")
            if cursor.hasSelection():
                temp = cursor.blockNumber()
                cursor.setPosition(cursor.anchor())
                diff = cursor.blockNumber() - temp
                direction = QtGui.QTextCursor.Up if diff > 0 else QtGui.QTextCursor.Down
                for _ in range(abs(diff) + 1):
                    line_length = self.get_line_length(cursor)
                    blank_number = int(((max_length - line_length) // 2) // 8)
                    if constants.DEBUG_RICHTEXT:
                        print("max length, line length, blank number", max_length, line_length, blank_number)
                    cursor.movePosition(QtGui.QTextCursor.StartOfLine)
                    cursor.insertText(" " * blank_number)
                    cursor.movePosition(QtGui.QTextCursor.EndOfLine)
                    cursor.insertText(" " * blank_number)
                    cursor.movePosition(direction)
                    self.setTextCursor(cursor)
            else:
                line_length = self.get_line_length(cursor)
                blank_number = int(((max_length - line_length) // 2) // 8)
                if constants.DEBUG_RICHTEXT:
                    print("max length, line length, blank number", max_length, line_length, blank_number)
                cursor.movePosition(QtGui.QTextCursor.StartOfLine)
                cursor.insertText(" " * blank_number)
                cursor.movePosition(QtGui.QTextCursor.EndOfLine)
                cursor.insertText(" " * blank_number)
                self.setTextCursor(cursor)
        elif align == "Left":
            self.align("Clean")
            if cursor.hasSelection():
                temp = cursor.blockNumber()
                cursor.setPosition(cursor.anchor())
                diff = cursor.blockNumber() - temp
                direction = QtGui.QTextCursor.Up if diff > 0 else QtGui.QTextCursor.Down
                for _ in range(abs(diff) + 1):
                    cursor.movePosition(QtGui.QTextCursor.StartOfLine)
                    line = cursor.block().text()
                    for char in line[:]:
                        if char != " ":
                            break
                        cursor.deleteChar()
                    cursor.movePosition(direction)
                    self.setTextCursor(cursor)
            else:
                cursor.movePosition(QtGui.QTextCursor.StartOfLine)
                line = cursor.block().text()
                for char in line:
                    if char != " ":
                        break
                    cursor.deleteChar()
                self.setTextCursor(cursor)
        elif align == "Right":
            self.align("Clean")
            if cursor.hasSelection():
                temp = cursor.blockNumber()
                cursor.setPosition(cursor.anchor())
                diff = cursor.blockNumber() - temp
                direction = QtGui.QTextCursor.Up if diff > 0 else QtGui.QTextCursor.Down
                for _ in range(abs(diff) + 1):
                    line_length = self.get_line_length(cursor)
                    blank_number = int((max_length - line_length) // 8)
                    cursor.movePosition(QtGui.QTextCursor.StartOfLine)
                    for _ in range(blank_number):
                        cursor.insertText(" ")
                    cursor.movePosition(direction)
                    self.setTextCursor(cursor)
            else:
                line_length = self.get_line_length(cursor)
                blank_number = int((max_length - line_length) // 8)
                cursor.movePosition(QtGui.QTextCursor.StartOfLine)
                for _ in range(blank_number):
                    cursor.insertText(" ")
                self.setTextCursor(cursor)
        elif align == "Clean":
            if cursor.hasSelection():
                temp = cursor.blockNumber()
                cursor.setPosition(cursor.anchor())
                diff = cursor.blockNumber() - temp
                direction = QtGui.QTextCursor.Up if diff > 0 else QtGui.QTextCursor.Down
                for _ in range(abs(diff) + 1):
                    cursor.movePosition(QtGui.QTextCursor.StartOfLine)
                    line = cursor.block().text()
                    for char in line:
                        if char != " ":
                            break
                        cursor.deleteChar()
                        if constants.DEBUG_RICHTEXT:
                            print("line: ", cursor.block().text(), len(cursor.block().text()))
                    index = len(line.strip())
                    if constants.DEBUG_RICHTEXT:
                        print("Before move: ", cursor.position(), index)
                    cursor.movePosition(QtGui.QTextCursor.Right, QtGui.QTextCursor.MoveAnchor, index)
                    if constants.DEBUG_RICHTEXT:
                        print("After move: ", cursor.position(), index, line.lstrip()[index:])
                    for char in line.lstrip()[index:]:
                        if char != " ":
                            break
                        cursor.deleteChar()
                        if constants.DEBUG_RICHTEXT:
                            print("line: ", cursor.block().text(), len(cursor.block().text()))
                    cursor.movePosition(direction)
                    self.setTextCursor(cursor)
            else:
                cursor.movePosition(QtGui.QTextCursor.StartOfLine)
                line = cursor.block().text()
                for char in line:
                    if char != " ":
                        break
                    cursor.deleteChar()
                    if constants.DEBUG_RICHTEXT:
                        print("line: ", cursor.block().text(), len(cursor.block().text()))
                index = len(line.strip())
                if constants.DEBUG_RICHTEXT:
                    print("Before move: ", cursor.position(), index)
                cursor.movePosition(QtGui.QTextCursor.Right, QtGui.QTextCursor.MoveAnchor, index)
                if constants.DEBUG_RICHTEXT:
                    print("After move: ", cursor.position(), index, line.lstrip()[index:])
                for char in line.lstrip()[index:]:
                    if char != " ":
                        break
                    cursor.deleteChar()
                    if constants.DEBUG_RICHTEXT:
                        print("line: ", cursor.block().text(), len(cursor.block().text()))
                self.setTextCursor(cursor)

    @staticmethod
    def latex_formula(str_latex):
        font_size = 8
        dpi = 300
        fig = pylab.figure()
        text = fig.text(0, 0, str_latex, fontsize=font_size)

        buff = io.BytesIO()
        fig.savefig(buff, format="png", dpi=dpi)
        bbox = text.get_window_extent()
        width, height = bbox.size / float(dpi) + 0.005
        fig.set_size_inches((width, height))
        dy = (bbox.ymin / float(dpi)) / height
        text.set_position((0, -dy))
        buff = io.BytesIO()
        fig.savefig(buff, format="png", dpi=dpi)

        buff.seek(0)
        img = plt.imread(buff)
        im = img.mean(axis=2)
        im = ((im - im.min()) / (im.ptp() / 255.0)).astype(np.uint8)
        temp_img = QtGui.QImage(im, im.shape[1], im.shape[0], im.shape[1], QtGui.QImage.Format_Indexed8)
        image = QtGui.QPixmap(temp_img).toImage()
        size = image.size()
        image = image.scaled(size.width() * 0.5, size.height() * 0.5,
                             QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
        return image

    def font_format(self, font_type):
        cursor = self.textCursor()
        text_format = QtGui.QTextCharFormat()
        if font_type == "Italic":
            if cursor.charFormat().fontItalic():
                text_format.setFontItalic(False)
            else:
                text_format.setFontItalic(True)
            cursor.mergeCharFormat(text_format)
            self.editing_state = False
        elif font_type == "Blod":
            if cursor.charFormat().fontWeight() == 50:
                text_format.setFontWeight(100)
            else:
                text_format.setFontWeight(50)
            cursor.mergeCharFormat(text_format)
            self.editing_state = False
        elif font_type == "Underline":
            if cursor.charFormat().fontUnderline():
                text_format.setFontUnderline(False)
            else:
                text_format.setFontUnderline(True)
                text_format.setUnderlineColor(QtGui.QColor(133, 255, 255))
            cursor.mergeCharFormat(text_format)
            self.editing_state = False
        elif font_type == "Deleteline":
            if cursor.charFormat().fontStrikeOut():
                text_format.setFontStrikeOut(False)
            else:
                text_format.setFontStrikeOut(True)
            cursor.mergeCharFormat(text_format)
            self.editing_state = False
        elif font_type == "Up":
            if constants.DEBUG_RICHTEXT:
                print("Font size: ", cursor.charFormat().fontPointSize())
            if cursor.charFormat().fontPointSize() == 0:
                font_point_size = 8
            else:
                font_point_size = cursor.charFormat().fontPointSize()
            point_size = font_point_size + 2
            text_format.setFontPointSize(point_size)
            cursor.mergeCharFormat(text_format)
            self.editing_state = True
            self.font_size_editing = True
        elif font_type == "Down":
            if constants.DEBUG_RICHTEXT:
                print("Font size: ", cursor.charFormat().fontPointSize())
            if cursor.charFormat().fontPointSize() == 0:
                font_point_size = 8
            else:
                font_point_size = cursor.charFormat().fontPointSize()
            point_size = font_point_size - 2 if font_point_size - 2 > 0 else 2
            text_format.setFontPointSize(point_size)
            cursor.mergeCharFormat(text_format)
            self.editing_state = True
            self.font_size_editing = True
        elif font_type == "Color":
            color = QtWidgets.QColorDialog.getColor(QtCore.Qt.red, None, "Select Color",
                                                    QtWidgets.QColorDialog.ShowAlphaChannel)
            if color:
                text_format.setForeground(color)
            cursor.mergeCharFormat(text_format)
            self.editing_state = False
        elif font_type == "Hyperlink":
            if not cursor.charFormat().isAnchor():
                text_format.setAnchor(True)
                text_format.setForeground(QtGui.QColor("Blue"))
                text_format.setAnchorHref(cursor.selection().toPlainText())
            else:
                text_format.setAnchor(False)
                text_format.setForeground(QtGui.QColor("Black"))
            cursor.mergeCharFormat(text_format)
            self.editing_state = False
        elif font_type == "Mathjax":
            str_latex = cursor.selection().toPlainText()
            if str_latex.startswith("$") and str_latex.endswith("$") and str_latex.count("$") == 2:
                img = self.latex_formula(str_latex)
                cursor.clearSelection()
                cursor.insertText("\n")
                cursor.insertImage(img)
                self.editing_state = False
        elif font_type == "Clear":
            cursor.setCharFormat(text_format)
            self.editing_state = False
        if not self.editing_state:
            cursor.movePosition(QtGui.QTextCursor.EndOfBlock)
            cursor.setCharFormat(QtGui.QTextCharFormat())
            self.setTextCursor(cursor)

    def image_format(self):
        cursor = self.textCursor()
        image_width = self.get_text_maxlength()
        image_height = 50
        if cursor.hasSelection():
            size_dialog = SizeDialog()
            text = cursor.selection().toHtml(bytes())
            if text.find(r'<img src=') != -1:
                cursor.removeSelectedText()
                if size_dialog.exec_():
                    image_width = size_dialog.num_width.text() if size_dialog.num_width.text() else image_width
                    image_height = size_dialog.num_height.text() if size_dialog.num_height.text() else image_height
                if constants.DEBUG_RICHTEXT:
                    print("image size: ", image_width, image_height)
                pattern = re.compile(r'<img src="(.+?)".+?/>')
                text = pattern.sub(r'<img src="\1" width="%s" height="%s" />' % (image_width, image_height), text)
                if constants.DEBUG_RICHTEXT:
                    print("*****************text***********************\n", text, "\n** \
                                                                                  ************************************")
                cursor.insertHtml(text)
            else:
                cursor.clearSelection()
                self.setTextCursor(cursor)

    @staticmethod
    def paste(cursor):
        mime_data = QtWidgets.QApplication.clipboard().mimeData()
        if mime_data.hasImage():
            image = QtGui.QImage(mime_data.imageData())
            cursor.insertImage(image)
        elif mime_data.hasUrls():
            for u in mime_data.urls():
                file_ext = os.path.splitext(str(u.toLocalFile()))[1].lower()
                if constants.DEBUG_RICHTEXT:
                    print(file_ext, u.isLocalFile())
                if u.isLocalFile() and file_ext in ('.jpg', '.png', '.bmp', '.icon', '.jpeg', 'gif'):
                    cursor.insertImage(u.toLocalFile())
                else:
                    break
            else:
                return
        elif mime_data.hasText():
            text = mime_data.text()
            cursor.insertText(text)
            if constants.DEBUG_RICHTEXT:
                print("PASTE: ", text)

    def keyPressEvent(self, event) -> None:
        # insert key text into text field.
        current_key = event.key()
        current_cursor = self.textCursor()

        # restore text before editing and return.
        if current_key == QtCore.Qt.Key_Escape:
            self.clearFocus()
            super(InputTextField, self).keyPressEvent(event)
            return
        elif current_key == QtCore.Qt.Key_BracketLeft and event.modifiers() & QtCore.Qt.ControlModifier:
            if constants.DEBUG_RICHTEXT:
                print("ALIGN LEFT")
            self.align("Left")
        elif current_key == QtCore.Qt.Key_BracketRight and event.modifiers() & QtCore.Qt.ControlModifier:
            if constants.DEBUG_RICHTEXT:
                print("ALIGN RIGHT")
            self.align("Right")
        elif current_key == QtCore.Qt.Key_Backslash and event.modifiers() & QtCore.Qt.ControlModifier:
            if constants.DEBUG_RICHTEXT:
                print("ALIGN CENTER")
            self.align("Center")
        elif current_key == QtCore.Qt.Key_P and event.modifiers() & QtCore.Qt.ControlModifier:
            if constants.DEBUG_RICHTEXT:
                print("ALIGN Clean")
            self.align("Clean")
        elif current_key == QtCore.Qt.Key_Q and event.modifiers() & QtCore.Qt.ControlModifier:
            if constants.DEBUG_RICHTEXT:
                print("Rich Format: Title")
            self.font_format("Italic")
        elif current_key == QtCore.Qt.Key_W and event.modifiers() & QtCore.Qt.ControlModifier:
            if constants.DEBUG_RICHTEXT:
                print("Rich Format: Title")
            self.font_format("Blod")
        elif current_key == QtCore.Qt.Key_R and event.modifiers() & QtCore.Qt.ControlModifier:
            if constants.DEBUG_RICHTEXT:
                print("Rich Format: Title")
            self.font_format("Underline")
        elif current_key == QtCore.Qt.Key_F and event.modifiers() & QtCore.Qt.ControlModifier:
            if constants.DEBUG_RICHTEXT:
                print("Rich Format: Title")
            self.font_format("Deleteline")
        elif current_key == QtCore.Qt.Key_G and event.modifiers() & QtCore.Qt.ControlModifier:
            if constants.DEBUG_RICHTEXT:
                print("Rich Format: Title")
            self.font_format("Up")
        elif current_key == QtCore.Qt.Key_H and event.modifiers() & QtCore.Qt.ControlModifier:
            if constants.DEBUG_RICHTEXT:
                print("Rich Format: Title")
            self.font_format("Down")
        elif current_key == QtCore.Qt.Key_N and event.modifiers() & QtCore.Qt.ControlModifier:
            if constants.DEBUG_RICHTEXT:
                print("Rich Format: Title")
            self.font_format("Color")
        elif current_key == QtCore.Qt.Key_O and event.modifiers() & QtCore.Qt.ControlModifier:
            if constants.DEBUG_RICHTEXT:
                print("Rich Format: Title")
            self.font_format("Hyperlink")
        elif current_key == QtCore.Qt.Key_Y and event.modifiers() & QtCore.Qt.ControlModifier:
            if constants.DEBUG_RICHTEXT:
                print("Rich Format: Title")
            self.font_format("Mathjax")
        elif current_key == QtCore.Qt.Key_L and event.modifiers() & QtCore.Qt.ControlModifier:
            if constants.DEBUG_RICHTEXT:
                print("Rich Format: Title")
            self.font_format("Clear")

        # todo: anchor and open link
        # todo: how to delete codeblock
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
        if current_key == QtCore.Qt.Key_M and event.modifiers() & QtCore.Qt.ControlModifier and current_table:
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

        # image
        if current_key == QtCore.Qt.Key_U and event.modifiers() & QtCore.Qt.ControlModifier:
            if constants.DEBUG_RICHTEXT:
                print("Rich Format: Image")
            self.image_format()

    def sceneEvent(self, event: QtCore.QEvent) -> bool:
        if event.type() == QtCore.QEvent.KeyPress:
            if event.matches(QtGui.QKeySequence.Paste):
                self.paste(self.textCursor())
                return False
            elif event.key() == QtCore.Qt.Key_Tab:
                if event.modifiers() == QtCore.Qt.ControlModifier:
                    if constants.DEBUG_RICHTEXT:
                        print("CTRL + TAB")
                    self.dedent()
                    return False
                else:
                    if constants.DEBUG_RICHTEXT:
                        print("TAB")
                    self.indent()
                    return False
            else:
                super(InputTextField, self).sceneEvent(event)
                return False
        else:
            super(InputTextField, self).sceneEvent(event)
            return False

    def mousePressEvent(self, event) -> None:
        # change focus into node
        hyperlink = self.textCursor().charFormat().isAnchor()
        if hyperlink:
            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.PointingHandCursor)
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
        hyperlink = self.textCursor().charFormat().isAnchor()
        if hyperlink:
            url = self.textCursor().charFormat().anchorHref()
            try:
                validators.url(url)
                QtGui.QDesktopServices.openUrl(QtCore.QUrl(url))
            except Exception as e:
                print("Valid hyperlink: ", e)
            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.ArrowCursor)
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
        super(InputTextField, self).focusOutEvent(event)
        self.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.setObjectName("Nothing")
        if constants.DEBUG_RICHTEXT:
            print("Html contents:\n", self.toHtml())
        if not self.editing_state or self.font_size_editing:
            cursor = self.textCursor()
            cursor.clearSelection()
            self.setTextCursor(cursor)
            self.font_size_editing = False
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
        #   sapcing
        self.layout.setSpacing(0)
        self.input_layout.setSpacing(0)
        self.output_layout.setSpacing(0)
        self.attribute_layout.setSpacing(0)
        #   margin
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.input_layout.setContentsMargins(0, 0, 0, 0)
        self.output_layout.setContentsMargins(0, 0, 0, 0)
        self.attribute_layout.setContentsMargins(0, 0, 0, 0)

        # WIDGETS
        #   title name widget
        self.attribute_widget = SubConstituteWidget(self)
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
        self.attribute_layout.addItem(self.attribute_widget)
        self.attribute_layout.setAlignment(self.attribute_widget, QtCore.Qt.AlignCenter)
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
