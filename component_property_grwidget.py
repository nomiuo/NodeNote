# extended
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsTextItem, QGraphicsRectItem
from PyQt5.QtGui import QColor, QBrush, QPen, QPainterPath, QPixmap
from PyQt5.QtCore import Qt, QRectF, QPointF

# size
width = 120
height = 40
egde = 5
title_height = 20
title_truth_x = 60
title_truth_width = 20
# color
outline_color = QColor("#FF9999FF")
outline_selected_color = QColor("#FFCC33FF")
title_color = QColor("#FF0099CC")
content_color = QColor("#FF80DFFF")


class PropertyGrwidget(QGraphicsItem):
    def __init__(self, parent=None):
        super(PropertyGrwidget, self).__init__(parent)
        self.gr_function()
        # add truth
        self.truth = PropertyGrwidgetTruth(self)
        self.add_truth()

    def gr_function(self):
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)

    def boundingRect(self): return QRectF(0, 0, width, height)

    def paint(self, painter, option, widget=None) -> None:
        outline_path = QPainterPath()
        outline_path.addRoundedRect(0, 0, width, height, egde, egde)

        outline_path.moveTo(0, title_height)
        outline_path.lineTo(width, title_height)

        painter.setBrush(QBrush(title_color))
        painter.setPen(outline_color if not self.isSelected() else outline_selected_color)
        painter.drawPath(outline_path)

    def add_truth(self):
        self.truth.setPos(title_truth_x, 0)


class PropertyGrwidgetTruth(QGraphicsItem):
    def __init__(self, parent=None):
        super(PropertyGrwidgetTruth, self).__init__(parent)
        self.truth = True

    def boundingRect(self): return QRectF(0, 0, title_truth_width, title_height)

    def paint(self, painter, option, widget=None) -> None:
        if self.truth:
            painter.drawPixmap(self.boundingRect(), QPixmap("Templates/right.png"), QRectF(0, 0, 250, 250))
        else:
            painter.drawPixmap(self.boundingRect(), QPixmap("Templates/wrong.png"), QRectF(0, 0, 250, 250))

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self.truth = not self.truth
            self.update()


class PropertyGrwidgetText(QGraphicsTextItem):
    def __init__(self, parent=None):
        super(PropertyGrwidgetText, self).__init__(parent)
