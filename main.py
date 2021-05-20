from Components.window import NoteWindow
from PyQt5.QtWidgets import QApplication


# todo: clone node
# todo: use time
# todo: paste
# todo: pic store logic
# todo: search
# todo: show after create sub scene
# todo: pipe deserialize control point
if __name__ == '__main__':
    app = QApplication([])
    window = NoteWindow()
    window.show()
    app.exec_()
