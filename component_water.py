from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QVariantAnimation, QSize, Qt, QPointF, QPoint
from PyQt5.QtGui import QColor, QPainter, QBrush, QPainterPath, QPalette


class Water(QWidget):
    def __init__(self, parent=None):
        super(Water, self).__init__(parent)

        # water ui
        self.water_color = QColor("#FF6699FF")
        self.circle_big_size = 10.0
        self.circle_small_size = 0.0
        self.design_ui()

        # water animation
        self.water_animation = QVariantAnimation(self)

    def design_ui(self):
        self.setFixedSize(QSize(int(self.circle_big_size * 2), int(self.circle_big_size * 2)))
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAutoFillBackground(True)
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(255, 255, 255, 255))
        self.setPalette(palette)
        self.setAttribute(Qt.WA_DeleteOnClose)

    def move(self, a0) -> None:
        true_pos = a0 - QPoint(int(self.circle_big_size), int(self.circle_big_size))
        super(Water, self).move(QPoint(true_pos.x(), true_pos.y()))

    def show(self):
        super(Water, self).show()
        self.water_animation.setStartValue(0.0)
        self.water_animation.setEndValue(self.circle_big_size)
        self.water_animation.setDuration(350)
        self.water_animation.valueChanged.connect(self.circle_repaint)
        self.water_animation.finished.connect(self.close)
        self.water_animation.start()

    def circle_repaint(self, value):
        self.circle_small_size = value
        self.update()

    def paintEvent(self, a0) -> None:
        # painter
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(self.water_color))
        # paint two circle
        big_circle = QPainterPath()
        big_circle.addEllipse(QPointF(self.circle_big_size, self.circle_big_size),
                              self.circle_big_size, self.circle_big_size)
        small_circle = QPainterPath()
        small_circle.addEllipse(QPointF(self.circle_big_size, self.circle_big_size),
                                self.circle_small_size, self.circle_small_size)
        circle = big_circle - small_circle
        painter.drawPath(circle)
