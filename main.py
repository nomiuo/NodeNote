import sys

from Components.window import NoteWindow
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication([])
    window = NoteWindow(sys.argv)
    window.show()
    app.exec_()