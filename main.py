from Components.window import NoteWindow
from PyQt5.QtWidgets import QApplication


# todo: clone node
# todo: use time
# todo: paste
# todo: pipe
# todo: move down and move up attribute widget
if __name__ == '__main__':
    app = QApplication([])
    window = NoteWindow()
    window.show()
    app.exec_()
