from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import QRect


class SnowWidget(QWidget):
    def __init__(self, parent=None):
        super(SnowWidget, self).__init__(parent)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), QPixmap('Templates/snow4.png'), QRect())


if __name__ == '__main__':
    app = QApplication([])
    sky = SnowWidget()
    sky.show()
    app.exec_()
