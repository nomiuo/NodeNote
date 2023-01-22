"""TestHandler tests handler like LoggerHandler.
"""

import sys
import traceback
import unittest
from unittest import TestCase

from PySide6 import QtCore, QtWidgets

from homes.controller.view.view import View


class TestHandler(TestCase):
    """TestHandler tests handler like LoggerHandler.

    Args:
        TestCase (class): Test class.
    """

    def test_logger_handler(self):
        """Test LoggerHandler."""
        app = QtWidgets.QApplication(sys.argv)
        View()
        app.exit(0)

        try:
            1 / 0
        except ZeroDivisionError:
            QtCore.qDebug(traceback.format_exc())


if __name__ == "__main__":
    unittest.main()
