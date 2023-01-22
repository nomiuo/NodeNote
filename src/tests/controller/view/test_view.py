import sys
import unittest
from unittest import TestCase

from PySide6 import QtWidgets

from homes.controller.view.view import View


class TestView(TestCase):
    def test_application(self):
        app = QtWidgets.QApplication(sys.argv)
        View()
        app.exit(0)


if __name__ == "__main__":
    unittest.main()
