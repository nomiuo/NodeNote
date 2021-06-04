from Components.window import NoteWindow
from PyQt5.QtWidgets import QApplication


# todo: clone node
# todo: use time
# todo: print
# todo: ball
if __name__ == '__main__':
    app = QApplication([])
    window = NoteWindow()
    window.show()
    app.exec_()
