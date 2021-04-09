import random
from PyQt5 import sip
from PyQt5.QtWidgets import QWidget, QGraphicsOpacityEffect, QApplication, QMainWindow
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, QPoint, QTimer
from snow_widget import SnowWidget


DEBUG = True


class SkyWidget(QWidget):
    timer = QTimer()

    def __init__(self, parent=None):
        super(SkyWidget, self).__init__(parent)
        self.path_list = list()
        self.index = 0
        self.timer.timeout.connect(self.snow_create)
        self.timer.start(8000)

    def snow_create(self):
        # DEBUG
        if DEBUG:
            print("1-Debug:    snow_create function running")
        # create snow widget and its path
        snow_widget = SnowWidget(self)
        opacity_snow = QGraphicsOpacityEffect(snow_widget)
        run_path = QPropertyAnimation(snow_widget, b"pos")
        opacity_path = QPropertyAnimation(opacity_snow, b"opacity")
        self.path_list.append(QParallelAnimationGroup())
        self.snow_falling(snow_widget, run_path, opacity_path, self.path_list[self.index])
        self.index += 1

    def snow_falling(self, snow_widget, run_path, opacity_path, path_group):
        # DEBUG
        if DEBUG:
            print("2-Debug:    snow_falling function running")
        # pos and size
        start_x = random.randint(0, int(self.width()))
        start_y = random.randint(0, int(self.height()))
        random_size = random.randint(0, 9)
        width = 24 if random_size >= 6 else (18 if random_size >= 3 else 12)
        height = 24 if random_size >= 6 else (18 if random_size >= 3 else 12)
        snow_widget.setGeometry(start_x, start_y, width, height)
        snow_widget.setVisible(True)

        # fall speed
        fall_time_run_path = random.randint(25000, 30000)
        fall_time_opacity_path = random.randint(25000, 30000)
        run_path.setStartValue(QPoint(start_x, start_y))
        run_path.setEndValue(QPoint(start_x, self.height()))
        run_path.setDuration(fall_time_run_path)
        run_path.setEasingCurve(QEasingCurve.InOutCubic)
        opacity_path.setStartValue(1)
        opacity_path.setEndValue(0)
        opacity_path.setDuration(fall_time_opacity_path)
        path_group.addAnimation(run_path)
        path_group.addAnimation(opacity_path)

        # falling
        path_group.start()
        path_group.finished.connect(lambda: self.snow_end(snow_widget))

    @staticmethod
    def snow_end(snow_widget):
        if DEBUG:
            print("3-Debug:    delete snow widget successfully")
        sip.delete(snow_widget)


if __name__ == '__main__':
    app = QApplication([])
    widget = QMainWindow()
    widget.setCentralWidget(SkyWidget())
    widget.setWindowOpacity(8)
    widget.show()
    app.exec_()
