__all__ = ["NoteWindow"]


from PyQt5 import QtWidgets, QtCore, QtGui
from Components.effect_snow import EffectSkyWidget
from Model import stylesheet
from GraphicsView.view import View


class NoteWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(NoteWindow, self).__init__()

        self.UI_MainWindow()

        # tool bar
        self.toolbar = QtWidgets.QToolBar()
        self.toolbar.setStyleSheet(stylesheet.STYLE_QTOOLBAR)
        self.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolbar)

        self.scene_list = QtWidgets.QTreeWidget()
        self.scene_list.setStyleSheet(stylesheet.STYLE_QTREEWIDGET)
        self.scene_list.setAlternatingRowColors(True)
        self.scene_list.setHeaderLabel("Scene List")
        self.scene_list.setIndentation(8)

        self.toolbar.addWidget(self.scene_list)
        self.toolbar.addSeparator()

        self.central_widget = QtWidgets.QWidget()  # central widget
        self.view_widget = View(self, self.central_widget)  # view widget
        self.scene_list.itemClicked.connect(self.view_widget.change_current_scene)
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

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() == QtCore.Qt.Key_B and int(a0.modifiers()) & QtCore.Qt.ControlModifier:
            self.toolbar.setVisible(not self.toolbar.isVisible())
        if a0.key() == QtCore.Qt.Key_Delete and len(self.scene_list.selectedItems()) == 1:
            self.view_widget.delete_sub_scene(self.scene_list.selectedItems()[0])
        super(NoteWindow, self).keyPressEvent(a0)

