from PyQt5.QtWidgets import QDesktopWidget, QVBoxLayout, QMainWindow
from PyQt5.QtGui import QIcon
from Scene_View.my_view import MyView
from Components.sky_widget import SkyWidget


class NoteWindow(QMainWindow):
    def __init__(self):
        super(NoteWindow, self).__init__()

        # function:1. basic Widget UI setting
        self.view_widget = MyView()  # view widget
        self.UI_Widget()

        # function: 2. basic MainWindow UI setting
        self.UI_MainWindow()

    # 1. basic Widget UI setting
    def UI_Widget(self):
        self.setCentralWidget(self.view_widget)  # set central

    # 2. basic MainWindow UI setting
    def UI_MainWindow(self):
        self.setWindowIcon(QIcon('./Templates/snow3.svg'))  # set icon
        self.setWindowTitle("Snow")  # set title
        self.resize(1200, 1000)  # set size
        self.move(  # set geometry
            (QDesktopWidget().screenGeometry().width() - self.geometry().width()) / 2,
            (QDesktopWidget().screenGeometry().height() - self.geometry().height()) / 2
        )
        self.setWindowOpacity(0.85)  # set opacity
