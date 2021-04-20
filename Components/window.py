__all__ = ["NoteWindow"]


from PyQt5 import QtWidgets, QtCore, QtGui
from Components.effect_snow import EffectSkyWidget
from GraphicsView.view import View


class NoteWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(NoteWindow, self).__init__()

        self.UI_MainWindow()

        self.central_widget = QtWidgets.QWidget()  # central widget
        self.view_widget = View(self.central_widget)  # view widget
        self.layout = QtWidgets.QVBoxLayout(self.central_widget)  # layout contains two widgets
        self.sky_widget = EffectSkyWidget(self.view_widget, self.central_widget)  # snow falling widget
        self.UI_Widget()

    def UI_MainWindow(self):
        self.setWindowIcon(QtGui.QIcon('Resources/snow3.svg'))  # set icon
        self.setWindowTitle("Snow")  # set title
        self.resize(1200, 1000)  # set size
        self.move(  # set geometry
            (QtWidgets.QDesktopWidget().screenGeometry().width() - self.geometry().width()) // 2,
            (QtWidgets.QDesktopWidget().screenGeometry().height() - self.geometry().height()) // 2
        )

    def UI_Widget(self):
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.view_widget)
        self.central_widget.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setCentralWidget(self.central_widget)

    def resizeEvent(self, a0) -> None:
        super(NoteWindow, self).resizeEvent(a0)
        self.sky_widget.resize(self.width(), self.height())
