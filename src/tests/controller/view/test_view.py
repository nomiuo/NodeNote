import sys
import unittest
from unittest import TestCase

from PySide6 import QtWidgets

from smiley.controller.scene.scene import Scene
from smiley.controller.view.view import View


class TestView(TestCase):
    def test_application(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.view = View()
        self.view.show()
        self.app.exec()
        self.assert_(True)


if __name__ == "__main__":
    unittest.main()
