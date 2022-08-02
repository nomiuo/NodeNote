"""View controller.
"""

import threading
from typing import Optional

from PySide6 import QtWidgets


class View(QtWidgets.QGraphicsView):
    """_summary_

    Args:
        QtWidgets (_type_): _description_
    """

    # Singleton lock.
    __instance_lock = threading.Lock()

    def get_singleton_instance(cls, parent: Optional[QtWidgets.QWidget]):
        """Create single view instance.

        Args:
            parent (Optional[QtWidgets.QWidget]): Parent widget.

        Returns:
            QGraphicsView: Singleton view.
        """
        with cls.__instance_lock:
            if not hasattr(View, "__instance"):
                cls.__instance = View(parent)
            return cls.__instance

    def __init__(self, parent: Optional[QtWidgets.QWidget]):
        super().__init__(parent)
