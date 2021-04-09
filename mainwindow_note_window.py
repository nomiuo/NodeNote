from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtGui import QIcon
from component_sky_widget import *


class NoteWindow(QMainWindow):
    def __init__(self):
        super(NoteWindow, self).__init__()

        # function: 1. basic MainWindow UI setting
        self.UI_MainWindow()

        # function: 2. basic Widget UI setting
        # self.view_widget = MyView()  # view widget
        # self.central_widget = QWidget()  # central widget
        # self.layout = QVBoxLayout()  # layout contains two widgets
        # self.sky_widget = SkyWidget()  # snow falling widget
        self.UI_Widget()

    # 1. basic MainWindow UI setting
    def UI_MainWindow(self):
        self.setWindowIcon(QIcon('Templates/snow3.svg'))  # set icon
        self.setWindowTitle("Snow")  # set title
        self.resize(1200, 1000)  # set size
        self.move(  # set geometry
            (QDesktopWidget().screenGeometry().width() - self.geometry().width()) // 2,
            (QDesktopWidget().screenGeometry().height() - self.geometry().height()) // 2
        )
        self.setWindowOpacity(0.85)  # set opacity

    # 2. basic Widget UI setting
    def UI_Widget(self):
        self.setCentralWidget(SkyWidget())


if __name__ == '__main__':
    app = QApplication([])
    window = NoteWindow()
    window.show()
    app.exec_()
