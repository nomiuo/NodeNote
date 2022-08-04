import sys
import unittest
from unittest import TestCase

from PySide6 import QtWidgets
from smiley.controller.scene.scene import Scene
from smiley.controller.view.view import View


class TestView(TestCase):
    def test_application(self):
        app = QtWidgets.QApplication(sys.argv)
        view = View.get_singleton_instance()
        view.show()
        app.exec()
        self.assert_(True)


if __name__ == "__main__":
    unittest.main()
