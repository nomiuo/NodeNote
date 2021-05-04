from PyQt5 import QtWidgets, QtGui, QtCore


__all__ = ["Scene"]


class Scene(QtWidgets.QGraphicsScene):
    def __init__(self, view, parent=None):
        super(Scene, self).__init__(parent)
        self.view = view
        self.setSceneRect(self.itemsBoundingRect())

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
