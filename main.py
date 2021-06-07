from Components.window import NoteWindow
from PyQt5.QtWidgets import QApplication


# todo: 1. clone node
# todo: 2. use time
# todo: 3. debug for change current scene background
if __name__ == '__main__':
    app = QApplication([])
    window = NoteWindow()
    window.show()
    app.exec_()
