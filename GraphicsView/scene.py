from PyQt5 import QtWidgets, QtGui


__all__ = ["Scene"]


class Scene(QtWidgets.QGraphicsScene):
    def __init__(self, view, parent=None):
        super(Scene, self).__init__(parent)
        self.view = view
        self.width = 64000
        self.height = 64000
        self.setSceneRect(-self.width // 2, -self.height // 2, self.width, self.height)
        self.background_img = QtGui.QPixmap("Resources/night.jpg")
        self.setBackgroundBrush(QtGui.QBrush(self.background_img))

        self.tuple_node_widget = list()
        self.pipe_widget = list()

    def add_tuple_node_widget(self, widget):
        self.tuple_node_widget.append(widget)

    def remove_tuple_node_widget(self, widget):
        self.tuple_node_widget.remove(widget)
        self.removeItem(widget)

    def add_pipe_widget(self, widget):
        self.pipe_widget.append(widget)
        self.removeItem(widget)

    def remove_pip_widget(self, widget):
        self.pipe_widget.remove(widget)
        self.removeItem(widget)
