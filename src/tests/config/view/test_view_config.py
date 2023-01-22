import sys
import unittest
from unittest import TestCase

from PySide6 import QtWidgets

from homes.config.controller.view_config import ViewConfig
from homes.controller.view.view import View


class TestViewConfig(TestCase):
    def test_render_config(self):
        app = QtWidgets.QApplication(sys.argv)
        view_config = ViewConfig().set_drag_mode(
            QtWidgets.QGraphicsView.DragMode.RubberBandDrag
        )
        view = View()
        view_config.drag_mode_config(view=view)
        app.exit(0)


if __name__ == "__main__":
    unittest.main()
