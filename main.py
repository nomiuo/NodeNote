import sys
from PyQt5.QtWidgets import QApplication
from Window.note_window import NoteWindow


if __name__ == '__main__':
    app = QApplication([])
    window = NoteWindow()
    window.show()
    sys.exit(app.exec_())
