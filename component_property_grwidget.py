from PyQt5.QtWidgets import QGraphicsItem, QCheckBox, QGraphicsProxyWidget
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QBrush, QPen, QColor, QPainterPath


class PropertyGrwidget(QGraphicsItem):
    def __init__(self, parent=None):
        super(PropertyGrwidget, self).__init__(parent)

        # 1.paint
        #   size
        self.height = 25
        self.width = 100
        self.edge = 10
        #   checkbox
        #       paint
        self.checkbox_height = 25
        self.checkbox_width = 25
        self.checkbox_edge = 10
        self.checkbox_brush = QBrush(QColor("#FF00FFCC"))
        #       widget
        self.checkbox = QCheckBox()
        self.gr_checkbox = QGraphicsProxyWidget(self)
        self.add_checkbox_widget()
        #   outline
        self.outline_color = QColor("#FFCCF5FF")
        self.outline_selected_color = QColor("#FF3399FF")
        # 2.function
        self.set_function()

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, self.width, self.height)

    def paint(self, painter, option, widget=None) -> None:
        # checkbox
        checkbox_path = QPainterPath()
        checkbox_path.setFillRule(Qt.WindingFill)
        checkbox_path.addRoundedRect(0, 0, self.checkbox_width, self.checkbox_height,
                                     self.checkbox_edge, self.checkbox_edge)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.checkbox_brush)
        painter.drawPath(checkbox_path)
        # outline
        outline_path = QPainterPath()
        outline_path.addRoundedRect(0, 0, self.width, self.height, self.edge, self.edge)
        painter.setPen(QPen(self.outline_color) if not self.isSelected() else QPen(self.outline_selected_color))
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(outline_path)

    def add_checkbox_widget(self):
        self.checkbox.setGeometry(0, 0, self.checkbox_width, self.checkbox_height)
        self.gr_checkbox.setWidget(self.checkbox)

    def add_textedit_widget(self):
        pass

    def add_label_widget(self):
        pass

    def set_function(self):
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
