from PySide6 import QtWidgets


class Scene(QtWidgets.QGraphicsScene):
    """Instance of scene stores all items in this white board.



    Args:
        QtWidgets.QGraphicsScene (class): Parent class which can manage all items.
    """

    def add_item_directly(
        self,
        item: QtWidgets.QGraphicsItem,
    ):
        self.addItem(item)
