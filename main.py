from Components.window import NoteWindow
from PyQt5.QtWidgets import QApplication


# todo: debug for pipe
# todo: timer
# todo: resize pipe
if __name__ == '__main__':
    app = QApplication([])
    window = NoteWindow()
    window.show()
    app.exec_()
