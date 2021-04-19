from PyQt5.QtWidgets import QDesktopWidget, QVBoxLayout, QMainWindow, QApplication
from PyQt5.QtGui import QIcon
from Components.effect_snow import *
from GraphicsView.view import MyView


class NoteWindow(QMainWindow):
    def __init__(self):
        super(NoteWindow, self).__init__()

        # function: 1. basic MainWindow UI setting
        self.UI_MainWindow()

        # function: 2. basic Widget UI setting
        self.central_widget = QWidget()  # central widget
        self.view_widget = MyView(self.central_widget)  # view widget
        self.layout = QVBoxLayout(self.central_widget)  # layout contains two widgets
        self.sky_widget = EffectSkyWidget(self.view_widget, self.central_widget)  # snow falling widget
        self.UI_Widget()

    # 1. basic MainWindow UI setting
    def UI_MainWindow(self):
        self.setWindowIcon(QIcon('Resources/snow3.svg'))  # set icon
        self.setWindowTitle("Snow")  # set title
        self.resize(1200, 1000)  # set size
        self.move(  # set geometry
            (QDesktopWidget().screenGeometry().width() - self.geometry().width()) // 2,
            (QDesktopWidget().screenGeometry().height() - self.geometry().height()) // 2
        )

    # 2. basic Widget UI setting
    def UI_Widget(self):
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.view_widget)
        self.central_widget.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setCentralWidget(self.central_widget)

    def resizeEvent(self, a0) -> None:
        super(NoteWindow, self).resizeEvent(a0)
        self.sky_widget.resize(self.width(), self.height())


if __name__ == '__main__':
    app = QApplication([])
    window = NoteWindow()
    window.show()
    app.exec_()
